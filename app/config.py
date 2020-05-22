"""Opearting system module."""
import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    """App configuration variables."""

    # database
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_HOST = os.getenv('DB_HOST')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    # app secret key
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    # mail server
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # administrator list
    ADMINS = os.getenv('ADMINS')


class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing the application."""

    DEBUG = True
    TESTING = True


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
