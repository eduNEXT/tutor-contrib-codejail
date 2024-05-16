"""Module with the configuration of config classes."""
from codejailservice.config import BaseConfig


class DevelopmentConfig(BaseConfig):
    """Class to use for development context that inherits from BaseConfig."""

    {{patch("codejail-common-settings")}}
    {{patch("codejail-development-settings")}}


class ProductionConfig(BaseConfig):
    """Class to use for production context that inherits from BaseConfig."""

    {{patch("codejail-common-settings")}}
    {{patch("codejail-production-settings")}}
