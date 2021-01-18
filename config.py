"""Opearting system module."""
import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """App configuration variables."""

    DEBUG = False
    TESTING = False
    DEBUG_TB_INTERCEPT_REDIRECTS = os.environ.get(
        'DEBUG_TB_INTERCEPT_REDIRECTS')

    SESSION_COOKIE_SECURE = True

    # database
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        'SQLALCHEMY_TRACK_MODIFICATIONS')

    # brokers
    RABBITMQ_URL = os.environ.get('RABBITMQ_URL')
    REDISTOGO_URL = os.environ.get('REDISTOGO_URL')

    # app secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # mail server
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')

    # administrator list
    ADMINS = os.environ.get('ADMINS')


class ProductionConfig(Config):
    """Production configurations."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEVELOPMENT = True
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    SESSION_COOKIE_SECURE = False

    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    RABBITMQ_URL = 'amqps://localhost//'
    REDISTOGO_URL = 'redis://localhost:6379'


class TestingConfig(Config):
    """Testing the application."""

    DEBUG_TB_INTERCEPT_REDIRECTS = True
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SECRET_KEY = os.environ.get('DEV_SECRET_KEY')
    DB_NAME = os.environ.get('TEST_DB_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')


class StagingConfig(Config):
    """Configurations for Staging."""

    DEVELOPMENT = True
    DEBUG = True


class ReleaseConfig(Config):
    """Releasing app configurations."""


app_config = dict(
    testing=TestingConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
    staging=StagingConfig,
    release=ReleaseConfig
)
