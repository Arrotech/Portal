import os
from os import path
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from instance.config import app_config


toolbar = DebugToolbarExtension()
db = SQLAlchemy()
jwtmanager = JWTManager()
cors = CORS()
mail = Mail()


def exam_app(config_name=None):
    """Create the app."""
    app = Flask(__name__, instance_relative_config=True,
                template_folder='../../../templates')

    app.config.from_object(app_config[config_name])
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from app.api.v2 import models # noqa

    # Initialize Plugins
    db.init_app(app)
    toolbar.init_app(app)
    jwtmanager.init_app(app)
    cors.init_app(app)
    mail.init_app(app)
    Celery(app)

    # Include Routes
    from utils.utils import bad_request, page_not_found,\
        method_not_allowed, unprocessabe_entity, internal_server_error
    from app.api.v1 import portal_v1
    from app.api.v2 import portal_v2

    # Register Blueprints and Error Handlers
    app.register_blueprint(portal_v1, url_prefix='/api/v1/')
    app.register_blueprint(portal_v2, url_prefix='/api/v2/')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(422, unprocessabe_entity)
    app.register_error_handler(500, internal_server_error)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return app
