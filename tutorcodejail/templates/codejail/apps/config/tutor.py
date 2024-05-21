"""Module with the configuration of config classes."""
from codejailservice.config import DevelopmentConfig, ProductionConfig


class DevelopmentConfig(DevelopmentConfig):
    """Class to use for development context that inherits from DevelopmentConfig."""

    {{patch("codejail-common-settings")}}
    {{patch("codejail-development-settings")}}


class ProductionConfig(ProductionConfig):
    """Class to use for production context that inherits from ProductionConfig."""

    {{patch("codejail-common-settings")}}
    {{patch("codejail-production-settings")}}
