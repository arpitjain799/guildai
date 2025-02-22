# Plugins

Plugin support is providedy by `guild.plugin`:

    >>> import guild.plugin

## Enumerating plugins

Plugins can be registered by installing packages that provide entry
points for the "guild.plugins" group. For these tests, we want to
ensure we are only working with built-ins:

    >>> guild.plugin.limit_to_builtin()

Use `iter_plugins` to iterate through the list of available plugins:

    >>> sorted([name for name, _ in guild.plugin.iter_plugins()])
    ['config_flags',
     'cpu',
     'dask',
     'disk',
     'dvc',
     'exec_script',
     'gpu',
     'ipynb',
     'keras',
     'memory',
     'perf',
     'python_script',
     'quarto_document',
     'queue',
     'r_script',
     'resource_flags',
     'skopt']

## Plugin instances

You can get the plugin instance using `for_name`:

    >>> guild.plugin.for_name("gpu")
    <guild.plugins.gpu.GPUPlugin object ...>

There is only ever one plugin instance for a given name:

    >>> guild.plugin.for_name("gpu") is guild.plugin.for_name("gpu")
    True
