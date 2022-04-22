"""Module with the configuration of config classes."""
from base import BaseConfig


class DevConfig(BaseConfig):
    """Class to use for development context that inherits from BaseConfig."""


class ProductionConfig(BaseConfig):
    """Class to use for production context that inherits from BaseConfig."""
