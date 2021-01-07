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

    SESSION_COOKIE_SECURE = True

    # database
    DB_NAME = "school_portal"
    DB_USER = "postgres"
    DB_HOST = "localhost"
    DB_PASSWORD = "postgres20930988"

    # brokers
    RABBITMQ_LOCAL_URL = "amqps://localhost//"
    RABBITMQ_HOSTED_URL = "amqps://wmznztra:2jFJ5RUUV4daZWzPWLcW5bczw2vFP2CJ@moose.rmq.cloudamqp.com/wmznztra"
    REDISTOGO_LOCAL_URL = "redis://localhost:6379"
    REDISTOGO_HOSTED_URL = "redis://redistogo:e321b5418c64a7495955088ac41a8a1b@pike.redistogo.com:11205/"

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


class TestingConfig(Config):
    """Testing the application."""

    TESTING = True
    SESSION_COOKIE_SECURE = False

    DB_NAME = 'test_school_portal'


class StagingConfig(Config):
    """Configurations for Staging."""


class ReleaseConfig(Config):
    """Releasing app configurations."""


app_config = dict(
    testing=TestingConfig,
    development=DevelopmentConfig,
    production=ProductionConfig,
    staging=StagingConfig,
    release=ReleaseConfig
)
