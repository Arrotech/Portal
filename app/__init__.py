"""Import flask module."""
from flask import Flask, jsonify, make_response, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api

from app.api.v1.views.auth_views import auth_v1
from app.api.v1.views.exam_views import exams_v1
from app.api.v1.views.library_views import books_v1
from app.api.v1.views.studentId_views import id_v1
from app.api.v1.views.fees_views import fees_v1
from app.api.v1.views.teachers_views import teachers_v1
from app.api.v1.views.subjects_view import subjects_v1
from app.config import app_config


def page_not_found(e):
    """Capture Not Found error."""
    return make_response(jsonify({
        "status": "400",
        "message": "resource not found"
    }), 404)

def method_not_allowed(e):
    """Capture Not Found error."""
    return make_response(jsonify({
        "status": "405",
        "message": "method not allowed"
    }), 405)

def exam_app(config_name):
    """Create the app."""
    app = Flask(__name__)
    CORS(app)

    app.config.from_pyfile('config.py')
    app.config["SECRET_KEY"] = 'schoolportal'
    jwt = JWTManager(app)

    api = Api(app)

    app.register_blueprint(auth_v1, url_prefix='/api/v1/auth/')
    app.register_blueprint(exams_v1, url_prefix='/api/v1/')
    app.register_blueprint(fees_v1, url_prefix='/api/v1/')
    app.register_blueprint(teachers_v1, url_prefix='/api/v1/auth/')
    app.register_blueprint(books_v1, url_prefix='/api/v1/')
    app.register_blueprint(subjects_v1, url_prefix='/api/v1/')
    app.register_blueprint(id_v1, url_prefix='/api/v1/')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    return app
