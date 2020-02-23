"""Import flask module."""
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
import os
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, Blueprint, render_template
from werkzeug.utils import secure_filename


from app.api.v1.views.auth_views import auth_v1
from app.api.v1.views.staff import auth
from app.api.v1.views.accountant import accountant
from app.api.v1.views.exam_views import exams_v1
from app.api.v1.views.library_views import books_v1
from app.api.v1.views.fees_views import fees_v1
from app.api.v1.views.subjects_view import subjects_v1
from app.config import app_config

app = Flask(__name__, template_folder='../templates')
app.config["IMAGE_UPLOADS"] = "/mnt/c/wsl/projects/pythonise/tutorials/flask_series/app/app/static/img/uploads"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


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

    CORS(app)

    app.config.from_pyfile('config.py')
    app.config["SECRET_KEY"] = 'schoolportal'

    app.register_blueprint(auth_v1, url_prefix='/api/v1/auth/')
    app.register_blueprint(auth, url_prefix='/api/v1/auth/staff/')
    app.register_blueprint(accountant, url_prefix='/api/v1/auth/accountant/')
    app.register_blueprint(exams_v1, url_prefix='/api/v1/')
    app.register_blueprint(fees_v1, url_prefix='/api/v1/')
    app.register_blueprint(books_v1, url_prefix='/api/v1/')
    app.register_blueprint(subjects_v1, url_prefix='/api/v1/')
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)

    return app


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        print(request.files)

        if request.files:

            if "filesize" in request.cookies:

                if not allowed_image_filesize(request.cookies["filesize"]):
                    print("Filesize exceeded maximum limit")
                    return redirect(request.url)

                image = request.files["image"]
                print(image.filename)

                if image.filename == "":
                    print("No filename")
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)

                    image.save(os.path.join(
                        app.config["IMAGE_UPLOADS"], filename))

                    print("Image saved")

                    return redirect(request.url)

                else:
                    print("That file extension is not allowed")
                    return redirect(request.url)

    return render_template("upload_image.html")
