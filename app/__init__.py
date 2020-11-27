"""Import flask module."""
import os
from os import path
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask import Flask

from utils.utils import bad_request, page_not_found, method_not_allowed, internal_server_error
from app.api.v1.models.database import Database
from app.api.v1 import portal_v1
from app.config import app_config

def exam_app(config_name='development'):
    """Create the app."""
    app = Flask(__name__, instance_relative_config=True,
                template_folder='../../../templates')

    # filling the config from a config file based on the environment: development, statging, testing, default
    # app.config.from_object(app_config[config_name])

    # filling the config from a config file: Secure data/information
    app.config.from_pyfile('config.py', silent=True)

    app.config['SECRET_KEY'] = "schoolportal"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

    CORS(app)
    JWTManager(app)
    Mail(app)

    Database().create_table()

    app.register_blueprint(portal_v1, url_prefix='/api/v1/')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return app



