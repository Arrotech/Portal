"""Import flask module."""
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from app.api.v1.models.database import Database
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, Blueprint, render_template
from werkzeug.utils import secure_filename
from utils.utils import bad_request, page_not_found, method_not_allowed, internal_server_error


from app.api.v1 import auth_v1
from app.api.v1 import staff_v1
from app.api.v1 import accountant_v1
from app.api.v1 import exams_v1
from app.api.v1 import books_v1
from app.api.v1 import fees_v1
from app.api.v1 import subjects_v1
from app.api.v1 import units_blueprint_v1
from app.config import app_config


def exam_app(config_name):
    """Create the app."""
    app = Flask(__name__, template_folder='../templates')
    app.config.from_pyfile('config.py')
    app.config["SECRET_KEY"] = 'schoolportal'

    CORS(app)
    JWTManager(app)

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
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, internal_server_error)

    return app
