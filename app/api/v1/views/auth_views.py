import json
from flask import make_response, jsonify, request, Blueprint, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.users_model import UsersModel
from utils.authorization import admin_required
from utils.utils import check_update_user_keys, is_valid_email, raise_error, check_register_keys, form_restrictions, is_valid_password, check_promote_student_keys
import datetime
from werkzeug.security import check_password_hash
from app.api.v1 import auth_v1
from utils.serializer import Serializer


@auth_v1.route('/register', methods=['POST', 'GET'])
def signup():
    """A new user can create a new account."""
    errors = check_register_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    surname = details['surname']
    admission_no = details['admission_no']
    email = details['email']
    password = details['password']
    form = details['form']
    stream = details['stream']
    if details['firstname'].isalpha() is False:
        return raise_error(400, "firstname is in wrong format")
    if details['lastname'].isalpha() is False:
        return raise_error(400, "lastname is in wrong format")
    if details['surname'].isalpha() is False:
        return raise_error(400, "surname is in wrong format")
    if not is_valid_email(email):
        return raise_error(400, "Invalid Email Format!")
    if not is_valid_password(password):
        return raise_error(400, "Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!")
    user_admission_no = json.loads(UsersModel().get_admission_no(admission_no))
    if user_admission_no:
        return raise_error(400, "Admission Number Already Exists!")
    user_email = json.loads(UsersModel().get_email(email))
    if user_email:
        return raise_error(400, "Email Already Exists!")
    if (form_restrictions(form) is False):
        return raise_error(400, "Form should be 1, 2, 3 or 4")
    user = json.loads(UsersModel(firstname, lastname, surname,
                                 admission_no, email, password, form, stream).save())
    return make_response(jsonify({
        "message": "Account created successfully!",
        "status": "201",
        "user": user
    }), 201)


@auth_v1.route('/login', methods=['POST'])
def login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(UsersModel().get_email(email))
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            expires = datetime.timedelta(days=365)
            token = create_access_token(identity=email, expires_delta=expires)
            refresh_token = create_refresh_token(
                identity=email, expires_delta=expires)
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


@auth_v1.route('/forgot', methods=['POST'])
def forgot():
    url = request.host_url + 'reset/'
    details = request.get_json()
    email = details['email']
    user = json.loads(UsersModel().get_email(email))
    if user:
        expires = datetime.timedelta(days=1)
        email_token = create_access_token(
            identity=email, expires_delta=expires)
        return make_response(jsonify({
            "status": "200",
            "message": "Check Your Email for the Password Reset Link",
            "token": email_token
        }), 200)

    return make_response(jsonify({
        "status": "200",
        "message": "Check Your Email for the Password Reset Link"
    }), 200)


@auth_v1.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    expires = datetime.timedelta(days=365)
    access_token = create_access_token(current_user, expires_delta=expires)
    ret = {
        'access_token': access_token
    }
    return jsonify(ret), 200


@auth_v1.route('/protected', methods=['GET'])
@jwt_required
def protected():
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200


@auth_v1.route('/users', methods=['GET'])
@jwt_required
@admin_required
def get_users():
    """An admin can fetch all users."""
    users = json.loads(UsersModel().get_users())
    return make_response(jsonify({
        "status": "200",
        "message": "successfully retrieved",
        "Users": users
    }), 200)


@auth_v1.route('/users/<string:admission_no>', methods=['GET'])
@jwt_required
def get_user(admission_no):
    """An admin can fetch a single user."""
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        return make_response(jsonify({
            "status": "200",
            "message": "successfully retrieved",
            "user": user
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "User Not Found"
    }), 404)


@auth_v1.route('/users/<string:admission_no>/promote', methods=['PUT'])
@jwt_required
def promote(admission_no):
    """An admin can promote a student to another form."""
    errors = check_promote_student_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    form = details['form']
    stream = details['stream']
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        updated_user = json.loads(
            UsersModel().promote_user(form, stream, admission_no))
        return make_response(jsonify({
            "status": "200",
            "message": "student promoted successfully",
            "user": updated_user
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "student not found"
    }), 404)


@auth_v1.route('/users/user_info/<int:user_id>', methods=['PUT'])
@jwt_required
def update_user_info(user_id):
    """Update user information."""
    errors = check_update_user_keys(request)
    if errors:
        return Serializer.serialize(errors, 400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    surname = details['surname']
    response = UsersModel().update_user_info(firstname, lastname, surname, user_id)
    if response:
        return Serializer.serialize(response, 200, "User updated successfully")
    return Serializer.serialize(response, 404, "User not found")


@auth_v1.route('/users/change_password/<int:user_id>', methods=['PUT'])
@jwt_required
def update_password(user_id):
    """Already existing user can update their password."""
    details = request.get_json()
    password = details['password']
    user = UsersModel().get_user_id(user_id)
    response = UsersModel().update_user_password(password, user_id)
    if response:
        return Serializer.serialize(response, 200, "Password updated successfully")
    return raise_error(404, "User not found")

