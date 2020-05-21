import json
import os
from datetime import datetime, timedelta
from flask import make_response, jsonify, request, Blueprint, render_template, url_for, redirect
from flask_jwt_extended import decode_token, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.users_model import UsersModel
from utils.authorization import admin_required
from utils.utils import default_decode_token, default_encode_token, generate_url, check_update_user_keys, is_valid_email, raise_error, check_register_keys, form_restrictions, is_valid_password, check_promote_student_keys
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.v1 import auth_v1
from utils.serializer import Serializer
from itsdangerous import URLSafeTimedSerializer
from app.__init__ import exam_app
from app.api.v1.services.mails.mail_services import send_email


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
    gender = details['gender']
    email = details['email']
    password = details['password']
    current_year = details['current_year']
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
    user = json.loads(UsersModel(firstname, lastname, surname,
                                 admission_no, gender, email, password, current_year).save())
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('auth_v1.confirm_email', token=token)
    send_email('Confirm Your Email',
               sender='arrotechdesign@gmail.com',
               recipients=[email],
               text_body=render_template(
                   'email_confirmation.txt', confirm_url=confirm_url),
               html_body=render_template('email_confirmation.html', confirm_url=confirm_url))
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
            expires = timedelta(days=365)
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


@auth_v1.route('/confirm/<token>')
def confirm_email(token):
    """Confirm email."""
    try:
        email = default_decode_token(token, salt='email-confirm-key', expiration=3600)
    except:
        return raise_error(404, "User not found")
    user = json.loads(UsersModel().get_email(email))
    user_id = user['user_id']
    if user:
        response = json.loads(UsersModel().confirm_email(
            user_id, is_confirmed=True))
        return make_response(jsonify({
            "status": "200",
            "message": "You have confirmed your email successfully",
            "is_confirmed": response
        }), 200)
    return raise_error(404, "User not found")


@auth_v1.route('/forgot', methods=['POST'])
def send_reset_email():
    """Send email for password reset link."""
    url = request.host_url + 'reset/'
    details = request.get_json()
    email = details['email']
    if not is_valid_email(email):
        return raise_error(400, "Invalid Email Format!")
    user = json.loads(UsersModel().get_email(email))
    if user:
        user_id = user['user_id']
        email = user['email']
        expires = timedelta(days=1)
        reset_token = create_access_token(
            identity=user_id, expires_delta=expires)
        send_email('Reset your password',
                   sender='arrotechdesign@gmail.com',
                   recipients=[email],
                   text_body=render_template(
                       'reset_password.txt', url=url + reset_token),
                   html_body=render_template('reset_password.html', url=url + reset_token))
        return make_response(jsonify({
            "status": "200",
            "message": "Check Your Email for the Password Reset Link"
        }), 200)
    return make_response(jsonify({
        "status": "200",
        "message": "Check Your Email for the Password Reset Link"
    }), 200)


@auth_v1.route('/reset', methods=['POST'])
def reset_password():
    """Reset password."""
    """Already existing user can update their password."""
    url = request.host_url + 'reset/'
    details = request.get_json()
    reset_token = details['reset_token']
    password = details['password']
    u_id = decode_token(reset_token)['identity']
    user = json.loads(UsersModel().get_user_id(user_id=u_id))
    if user:
        email = user['email']
        user_id = user['user_id']
        hashed_password = generate_password_hash(password)
        response = json.loads(
            UsersModel().update_user_password(hashed_password, user_id))
        send_email('Password reset successful',
                   sender='arrotechdesign@gmail.com',
                   recipients=[email],
                   text_body='Password reset was successful',
                   html_body='<p>Password reset was successful</p>')
        return make_response(jsonify({
            "status": "200",
            "message": "Password reset successful",
            "user": response
        }))
    return make_response(jsonify({
        "status": "404",
        "message": "User not found"
    }))


@auth_v1.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    expires = timedelta(days=365)
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
    current_year = details['current_year']
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        updated_user = json.loads(
            UsersModel().promote_user(current_year, admission_no))
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
