# Install test dependencies

Tests require additional packages that are not included in the Guild
distribution or requirements.txt. They are defined in
guild/tests/requirements.txt.

    >>> test_reqs = path(guild.__pkgdir__, "guild/tests/requirements.txt")
    >>> quiet(f"pip install -r '{test_reqs}'")

Verify Guild info across supported environments. Note that only some
versions are asserted to varying degrees. These assertions roughly
correspond to stable ranges where we're interested in changes.

Python 3.7:

    >>> run("guild check --verbose --offline")  # doctest: -PY3 +PY37
    guild_version:             ...
    psutil_version:            5.9...
    tensorboard_version:       2.11...
    cuda_version:              ...
    nvidia_smi_version:        ...
    click_version:             8.1...
    dask_version:              2022...
    distutils_version:         ...
    numpy_version:             1.21...
    pandas_version:            1.3...
    pip_version:               ...
    sklearn_version:           1.0...
    setuptools_version:        ...
    twine_version:             4.0...
    yaml_version:              6.0
    werkzeug_version:          2...
    latest_guild_version:      ...

Python 3.8:

    >>> run("guild check --verbose --offline")  # doctest: -PY3 +PY38
    guild_version:             ...
    psutil_version:            5.9...
    tensorboard_version:       2.12...
    cuda_version:              ...
    nvidia_smi_version:        ...
    click_version:             8.1...
    dask_version:              2023...
    distutils_version:         ...
    numpy_version:             1.24...
    pandas_version:            2.0...
    pip_version:               ...
    sklearn_version:           1.2...
    setuptools_version:        ...
    twine_version:             4.0...
    yaml_version:              6.0
    werkzeug_version:          2...
    latest_guild_version:      ...

Python 3.9:

    >>> run("guild check --verbose --offline")  # doctest: -PY3 +PY39
    guild_version:             ...
    psutil_version:            5.9...
    tensorboard_version:       2.12...
    cuda_version:              ...
    nvidia_smi_version:        ...
    click_version:             8.1...
    dask_version:              2023...
    distutils_version:         ...
    numpy_version:             1.24...
    pandas_version:            2.0...
    pip_version:               ...
    sklearn_version:           1.2...
    setuptools_version:        ...
    twine_version:             4.0...
    yaml_version:              6.0
    werkzeug_version:          2...
    latest_guild_version:      ...

Python 3.10:

    >>> run("guild check --verbose --offline")  # doctest: -PY3 +PY310
    guild_version:             ...
    psutil_version:            5.9...
    tensorboard_version:       2.12...
    cuda_version:              ...
    nvidia_smi_version:        ...
    click_version:             8.1...
    dask_version:              2023...
    distutils_version:         ...
    numpy_version:             1.24...
    pandas_version:            2.0...
    pip_version:               ...
    sklearn_version:           1.2...
    setuptools_version:        ...
    twine_version:             4.0...
    yaml_version:              6.0
    werkzeug_version:          2...
    latest_guild_version:      ...

Python 3.11:

    >>> run("guild check --verbose --offline")  # doctest: -PY3 +PY311
    guild_version:             ...
    psutil_version:            5.9...
    tensorboard_version:       2.12...
    cuda_version:              ...
    nvidia_smi_version:        ...
    click_version:             8.1...
    dask_version:              2023...
    distutils_version:         ...
    numpy_version:             1.24...
    pandas_version:            2.0...
    pip_version:               ...
    sklearn_version:           1.2...
    setuptools_version:        ...
    twine_version:             4.0...
    yaml_version:              6.0
    werkzeug_version:          2...
    latest_guild_version:      ...
