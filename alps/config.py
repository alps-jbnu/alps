import pathlib
import warnings

from yaml import load

__all__ = 'read_config',


def read_config(config_path):
    if not isinstance(config_path, pathlib.Path):
        raise TypeError(
            'expected an instace of {1.__module__}.{1.__qualname__}'
            ', not {0!r}'.format(config_path, pathlib.Path)
        )
    if config_path.suffix not in ('.yml', '.yaml'):
        warnings.warn(
            'expected a YAML(.yml/.yaml) file, but the suffix of {0}'
            'doesn\'t represent YAML',
            RuntimeWarning, stacklevel=2
        )
    with config_path.open() as f:
        config_dict = load(f)
    return config_dict
