import json
from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.teachers_models import TeachersModel
from app.api.v1.models.revoked_tokens_model import RevokedToken
from utils.authorization import admin_required
from utils.utils import is_valid_email, raise_error, check_register_keys, form_restrictions, check_teachers_keys
import datetime
from werkzeug.security import check_password_hash

teachers_v1 = Blueprint('teachers_v1', __name__)


@teachers_v1.route('/register', methods=['POST', 'GET'])
def signup_teachers():
    """A new user can create a new account."""
    errors = check_teachers_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    email = details['email']
    password = details['password']
    form = details['form']
    role = details['role']
    if details['firstname'].isalpha() is False:
        return raise_error(400, "firstname is in wrong format")
    if details['lastname'].isalpha() is False:
        return raise_error(400, "lastname is in wrong format")
    if not is_valid_email(email):
        return raise_error(400, "Invalid Email Format!")
    if len(details['password']) < 8:
        return raise_error(400, "length of password should be atleast eight characters")
    user_email = json.loads(TeachersModel().get_email(email))
    if user_email:
        return raise_error(400, "Email Already Exists!")
    if (form_restrictions(form) is False):
        return raise_error(400, "Form should be 1, 2, 3 or 4")
    user = json.loads(TeachersModel(firstname, lastname, email, password, form, role).save())
    return make_response(jsonify({
        "message": "Account created successfully!",
        "status": "201",
        "user": user
    }), 201)

@teachers_v1.route('/login', methods=['POST'])
def login_teachers():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(TeachersModel().get_email(email))
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            expires = datetime.timedelta(days=365)
            token = create_access_token(identity=email, expires_delta=expires)
            refresh_token = create_refresh_token(identity=email, expires_delta=expires)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "token": token,
                "refresh_token": refresh_token,
                "user": user
            }), 200)
        return make_response(jsonify({
            "status": "401",
            "message": "Invalid Email or Password"
        }), 401)
    return make_response(jsonify({
        "status": "401",
        "message": "Invalid Email or Password"
    }), 401)