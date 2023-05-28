"""Config file."""

from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel

import src


class Config(BaseModel):
    """Config class."""

    arguments: Dict[str, Dict[str, Any]]


def load_config(config_file: Optional[Path] = None) -> Config:
    """
    Get params from config.

    Args:
        config_file: Path for config file.

    Returns:
        Config: Object of config class.
    """
    default_file = Path(src.__file__).parent / 'config.yml'
    config_file = config_file or default_file

    raw = config_file.read_text(encoding='utf8')
    config = yaml.safe_load(raw)
    return Config(**config)
