import copy
import os
from pathlib import Path
from typing import Any

import yaml

from serps.constants import DEFAULT_CONFIG, USER_CONFIG_PATH


def merge_configs(default: dict[str, Any], overwrite: dict[str, Any]) -> dict[str, Any]:
    """Recursively update a dict with the key/value pair of another.

    Dict values that are dictionaries themselves will be updated, whilst
    preserving existing keys.
    """
    new_config = copy.deepcopy(default)

    for k, v in overwrite.items():
        if isinstance(v, dict):
            new_config[k] = merge_configs(default.get(k, {}), v)
        else:
            new_config[k] = v

    return new_config


def get_config(path: Path | str) -> dict[str, Any]:
    if not os.path.exists(path):
        print("No config")
        raise Exception

    with open(path, encoding="utf-8") as file:
        try:
            yaml_config = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            msg = f"Unable to parse YAML file {path}."
            raise Exception(msg) from e
        if not isinstance(yaml_config, dict):
            msg = f"Top-level element of YAML file {path} should be an object."
            raise Exception(msg)

    config = merge_configs(DEFAULT_CONFIG, yaml_config)

    return config


def get_user_config_path() -> Path:
    if "SERPS_CONFIG" in os.environ:
        return Path(os.environ["SERPS_CONFIG"])
    if "XDG_CONFIG_HOME" in os.environ:
        return Path(os.environ["XDG_CONFIG_HOME"]) / "serps/serpsrc"
    return USER_CONFIG_PATH


def save_user_config(config: dict[str, Any]) -> None:
    yaml_config = merge_configs(DEFAULT_CONFIG, config)
    config_file_path = get_user_config_path()
    if not config_file_path:
        config_file_path = USER_CONFIG_PATH
    os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
    with open(config_file_path, "w", encoding="utf-8") as file:
        yaml.dump(yaml_config, file, default_flow_style=False, sort_keys=False)


def get_user_config(
    config_file: str | None = None,
    default_config: bool | dict[str, Any] = False,
) -> dict[str, Any]:
    """Return the user config as a dict.

    If ``default_config`` is True, ignore ``config_file`` and return default
    values for the config parameters.

    If ``default_config`` is a dict, merge values with default values and return them
    for the config parameters.

    If a path to a ``config_file`` is given, that is different from the default
    location, load the user config from that.

    Otherwise look up the config file path in the ``SERPS_CONFIG``
    environment variable. If set, load the config from this path. This will
    raise an error if the specified path is not valid.

    If the environment variable is not set, try the default config file path
    before falling back to the default config values.
    """
    # Do NOT load a config. Merge provided values with defaults and return them instead
    if default_config and isinstance(default_config, dict):
        return merge_configs(DEFAULT_CONFIG, default_config)

    # Do NOT load a config. Return defaults instead.
    if default_config:
        return copy.copy(DEFAULT_CONFIG)

    # Load the given config file
    if config_file and config_file is not USER_CONFIG_PATH:
        return get_config(config_file)

    config_file_path = get_user_config_path()
    if not os.path.exists(config_file_path):
        save_user_config(DEFAULT_CONFIG)
        return copy.copy(DEFAULT_CONFIG)
    return get_config(config_file_path)
