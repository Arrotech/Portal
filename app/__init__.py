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
from app.api.v1 import auth_v1, staff_v1, accountant_v1, exams_v1, books_v1, fees_v1,\
    subjects_v1, units_blueprint_v1, hostels_v1, departments_v1, courses_v1, apply_course_v1,\
    accommodation_v1
from app.config import app_config


def exam_app(config_name):
    """Create the app."""
    app = Flask(__name__, template_folder='../../../templates')
    config_name = os.getenv('FLASK_ENV')
    if config_name == 'development':
        app.config.from_pyfile('config.py')
        app.config['SECRET_KEY'] = "schoolportal"
    elif config_name == 'testing':
        app.config.from_pyfile('config.py')
        app.config['SECRET_KEY'] = "schoolportal"
    else:
        app.config.from_pyfile('config.py')
        app.config['SECRET_KEY'] = "schoolportal"

    CORS(app)
    JWTManager(app)
    Mail(app)

    Database().create_table()

    app.register_blueprint(auth_v1, url_prefix='/api/v1/auth/')
    app.register_blueprint(staff_v1, url_prefix='/api/v1/auth/staff/')
    app.register_blueprint(
        accountant_v1, url_prefix='/api/v1/auth/accountant/')
    app.register_blueprint(exams_v1, url_prefix='/api/v1/')
    app.register_blueprint(fees_v1, url_prefix='/api/v1/')
    app.register_blueprint(books_v1, url_prefix='/api/v1/')
    app.register_blueprint(subjects_v1, url_prefix='/api/v1/')
    app.register_blueprint(units_blueprint_v1, url_prefix='/api/v1/')
    app.register_blueprint(hostels_v1, url_prefix='/api/v1/')
    app.register_blueprint(departments_v1, url_prefix='/api/v1/')
    app.register_blueprint(courses_v1, url_prefix='/api/v1/')
    app.register_blueprint(apply_course_v1, url_prefix='/api/v1/')
    app.register_blueprint(accommodation_v1, url_prefix='/api/v1/')
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, '.env'))

    return app
