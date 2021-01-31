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

    JSONIFY_PRETTYPRINT_REGULAR = False

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

    # chaos monkey
    CHAOS_MIDDLEWARE_APPLICATION_NAME = os.environ.get(
        'CHAOS_MIDDLEWARE_APPLICATION_NAME')
    CHAOS_MIDDLEWARE_APPLICATION_ENV = os.environ.get(
        'CHAOS_MIDDLEWARE_APPLICATION_ENV')
    CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN = os.environ.get(
        'CHAOS_MIDDLEWARE_PROOFDOCK_API_TOKEN')
    JSONIFY_PRETTYPRINT_REGULAR = os.environ.get(
        'JSONIFY_PRETTYPRINT_REGULAR')

    # google
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    ACCESS_TOKEN_URI = os.environ.get("ACCESS_TOKEN_URI", default=False)
    AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL", default=False)
    AUTHORIZATION_SCOPE = os.environ.get("AUTHORIZATION_SCOPE", default=False)
    AUTH_REDIRECT_URI = os.environ.get("AUTH_REDIRECT_URI", default=False)
    BASE_URI = os.environ.get("BASE_URI", default=False)
    AUTH_TOKEN_KEY = os.environ.get("AUTH_TOKEN_KEY", default=False)
    AUTH_STATE_KEY = os.environ.get("AUTH_STATE_KEY", default=False)

    # celery
    CELERY_CONFIG = {}


class ProductionConfig(Config):
    """Production configurations."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Allow debug to restart after changes."""

    DEVELOPMENT = True
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = True

    SESSION_COOKIE_SECURE = False

    # brokers
    RABBITMQ_URL = os.environ.get('LOCAL_RABBITMQ_URL')
    REDISTOGO_URL = os.environ.get('LOCAL_REDISTOGO_URL')


class TestingConfig(Config):
    """Testing the application."""

    DEBUG_TB_INTERCEPT_REDIRECTS = True
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    # database
    DB_NAME = os.environ.get('TEST_DB_NAME')
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')

    # celery
    CELERY_CONFIG = {'CELERY_ALWAYS_EAGER': True}


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
