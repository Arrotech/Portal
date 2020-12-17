"""Opearting system module."""
import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """App configuration variables."""

    DEBUG = True
    TESTING = False

    SESSION_COOKIE_SECURE = True
    ENV = 'production'
    FLASK_ENV= 'production'

    # database
    DB_NAME = "school_portal"
    DB_USER = "postgres"
    DB_HOST = "localhost"
    DB_PASSWORD = "postgres20930988"
    REDISTOGO_URL = "redis://localhost:6379"

    # app secret key
    SECRET_KEY = "schoolportal"
    JWT_SECRET_KEY = "jwtschoolportal"

    # mail server
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'arrotechdesign@gmail.com'
    MAIL_PASSWORD = '11371265!birkhoff?'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # administrator list
    ADMINS = ['arrotechdesign@gmail.com']


class ProductionConfig(Config):
    """Production configurations."""

class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEBUG = True
    SESSION_COOKIE_SECURE = False
    FLASK_ENV = 'development'
    ENV = 'development'


class TestingConfig(Config):
    """Testing the application."""

    TESTING = True
    SESSION_COOKIE_SECURE = False

    DB_NAME = 'test_school_portal'
    FLASK_ENV = 'testing'
    ENV = 'testing'


class StagingConfig(Config):
    """Configurations for Staging."""

    FLASK_ENV = 'staging'
    ENV = 'staging'


class ReleaseConfig(Config):
    """Releasing app configurations."""

    DEBUG = False
    FLASK_ENV = 'release'
    ENV = 'release'


app_config = dict(
    testing=TestingConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
    staging=StagingConfig,
    release=ReleaseConfig
)
