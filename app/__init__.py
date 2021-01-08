"""Import flask module."""
import os
from os import path
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.api.v1.models.database import Database
from app.config import app_config

db = SQLAlchemy()
migrate = Migrate()


def exam_app(config_name):
    """Create the app."""
    app = Flask(__name__, template_folder='../../../templates')

    if config_name == 'testing':
        app.config.from_object(app_config[config_name])
    elif config_name == 'development':
        app.config.from_object(app_config[config_name])
    elif config_name == 'production':
        app.config.from_object(app_config[config_name])
    elif config_name == 'staging':
        app.config.from_object(app_config[config_name])
    elif config_name == 'release':
        app.config.from_object(app_config[config_name])

    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)
    JWTManager(app)
    Celery(app)
    Mail(app)

    Database().create_table()

    from utils.utils import bad_request, page_not_found, method_not_allowed, internal_server_error
    from app.api.v1 import portal_v1

    app.register_blueprint(portal_v1, url_prefix='/api/v1/')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return app
