# Copyright 2017-2023 Posit Software, PBC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from guild import guildfile
from guild import op_util
from guild import plugin as pluginlib
from guild import util

from . import flags_import_util

log = logging.getLogger("guild")


class _ConfigNotSupported(Exception):
    def __str__(self):
        assert len(self.args) == 1
        return f"config type for {self.args[0]} not supported"


class ConfigFlagsPlugin(pluginlib.Plugin):
    def guildfile_loaded(self, gf):
        for m in gf.models.values():
            for opdef in m.operations:
                apply_config_flags(opdef)


def apply_config_flags(opdef):
    config_src = _config_src(opdef)
    if not config_src:
        return
    flags_import_util.apply_flags(opdef, lambda: _flags_data(config_src))
    _ensure_config_dep(config_src, opdef)


def _config_src(opdef):
    if opdef.flags_dest and opdef.flags_dest.startswith("config:"):
        return opdef.flags_dest[7:]
    return None


def _flags_data(src):
    data = _load_flags(src)
    return {
        name: flags_import_util.flag_data_for_val(val)
        for name, val in data.items()
        if _is_legal_flag_val(val)
    }


def _load_flags(src):
    ext = _flags_src_ext(src)
    if ext in (".yaml", ".yml"):
        return _load_flags_yaml(src)
    if ext in (".json",):
        return _load_flags_json(src)
    if ext in (".ini", ".cfg"):
        return _load_flags_cfg(src)
    raise _ConfigNotSupported(src)


def _flags_src_ext(src):
    ext = os.path.splitext(src)[1].lower()
    if ext == ".in":
        return _flags_src_ext(src[:-3])
    return ext


def _load_flags_yaml(src):
    import yaml

    data = yaml.safe_load(open(src))
    return dict(_iter_keyvals(data))


def _iter_keyvals(data):
    if not isinstance(data, dict):
        return
    for basename, val in data.items():
        if isinstance(val, dict):
            for name, val in _iter_keyvals(val):
                yield ".".join([basename, name]), val
        else:
            yield basename, val


def _load_flags_json(src):
    import json

    data = json.load(open(src))
    return dict(_iter_keyvals(data))


def _load_flags_cfg(src):
    import configparser

    config = configparser.ConfigParser(default_section=None)
    config.read(src)
    data = {}
    for section in config.sections():
        for name in config.options(section):
            val = util.decode_cfg_val(config.get(section, name))
            data[f"{section}.{name}"] = val
    return data


def _is_legal_flag_val(val):
    return val is None or isinstance(val, (str, int, float, bool, list))


def _ensure_config_dep(config_src, opdef):
    """Ensures that opdef is configured to resolve config src."""
    existing = _find_config_res_source(opdef, config_src)
    if existing:
        _ensure_config_dep_attrs(existing)
    else:
        _add_config_dep(config_src, opdef)


def _find_config_res_source(opdef, config_src):
    config_source_uri = f"config:{config_src}"
    for resdef in op_util.iter_opdef_resources(opdef):
        for source in resdef.sources:
            if source.uri == config_source_uri:
                return source
    return None


def _ensure_config_dep_attrs(source):
    """Ensures that a dep source is configured resolving a config.

    Specificlaly, sets 'always_resolve' and 'replace_existing' both to
    True if they are not alreay set. This ensures that a run restart
    will resolve any new flag values by re-resolving the config source.
    """
    if source.always_resolve is None:
        source.always_resolve = True
    if source.replace_existing is None:
        source.replace_existing = True


def _add_config_dep(config_src, opdef):
    """Adds a config dependency to opdef for a config source (path)."""
    opdef.dependencies.append(
        guildfile.OpDependencyDef(_op_dep_data(config_src), opdef)
    )


def _op_dep_data(config_src):
    data = {
        "config": config_src,
        "replace-existing": True,
        "always-resolve": True,
    }
    _maybe_set_target_path(config_src, data)
    return data


def _maybe_set_target_path(src, data):
    """Sets target-path in op def data if `src` is in a subdirectory.

    Guild assumes that if a config src is in a subdirectory (relative
    to the Guild file), the intent is to install the resolved config
    file in the run directory under the same relative path.

    For example, if a flags dest is `config:foo/bar/config.yml`, Guild
    will set `target-path` to `foo/bar` for the config dependency.
    """
    parent_dir = os.path.dirname(src)
    if parent_dir:
        data["target-path"] = parent_dir
