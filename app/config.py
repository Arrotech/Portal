"""Opearting system module."""
import os


class Config:
    """Config docstring."""

    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing the application."""

    DEBUG = True
    TESTING = True
    DB_NAME = os.getenv('DB_TEST_NAME')


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ReleaseConfig(Config):
    """Releasing app configurations."""

    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    """Production configurations."""

    pass


app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}
