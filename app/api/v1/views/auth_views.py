import json
import os
from datetime import datetime, timedelta
from flask import make_response, jsonify, request, Blueprint, render_template, url_for, redirect
from flask_jwt_extended import decode_token, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.users_model import UsersModel
from utils.authorization import admin_required
from utils.utils import default_decode_token, default_encode_token, generate_url, check_update_user_keys, is_valid_email, raise_error, check_register_keys, form_restrictions, is_valid_password, check_promote_student_keys
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from itsdangerous import URLSafeTimedSerializer
from app.__init__ import exam_app
from app.api.v1.services.mails.mail_services import send_email


@portal_v1.route('/students/register', methods=['POST', 'GET'])
@jwt_required
@admin_required
def student_signup():
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
    user_email = json.loads(UsersModel().get_user_by_email(email))
    if user_email:
        return raise_error(400, "Email Already Exists!")
    user = json.loads(UsersModel(firstname, lastname, surname,
                                 admission_no, gender, email, password).save_student())
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
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

@portal_v1.route('/staff/register', methods=['POST', 'GET'])
def admin_signup():
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
    user_email = json.loads(UsersModel().get_user_by_email(email))
    if user_email:
        return raise_error(400, "Email Already Exists!")
    user = json.loads(UsersModel(firstname, lastname, surname,
                                 admission_no, gender, email, password).save_admin())
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
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

@portal_v1.route('/accountant/register', methods=['POST', 'GET'])
@jwt_required
@admin_required
def accountant_signup():
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
    user_email = json.loads(UsersModel().get_user_by_email(email))
    if user_email:
        return raise_error(400, "Email Already Exists!")
    user = json.loads(UsersModel(firstname, lastname, surname,
                                 admission_no, gender, email, password).save_accountant())
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
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



@portal_v1.route('/students/login', methods=['POST'])
def student_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(UsersModel().get_user_by_email(email))
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

@portal_v1.route('/staff/login', methods=['POST'])
def staff_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(UsersModel().get_user_by_email(email))
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

@portal_v1.route('/accountant/login', methods=['POST'])
def accountant_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = json.loads(UsersModel().get_user_by_email(email))
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


@portal_v1.route('/students/confirm/<token>')
def confirm_email(token):
    """Confirm email."""
    try:
        email = default_decode_token(
            token, salt='email-confirm-key', expiration=3600)
    except:
        return raise_error(404, "User not found")
    user = json.loads(UsersModel().get_user_by_email(email))
    user_id = user['user_id']
    if user:
        response = json.loads(UsersModel().confirm_user_email(
            user_id, is_confirmed=True))
        return make_response(jsonify({
            "status": "200",
            "message": "You have confirmed your email successfully",
            "is_confirmed": response
        }), 200)
    return raise_error(404, "User not found")


@portal_v1.route('/students/forgot', methods=['POST'])
def send_reset_email():
    """Send email for password reset link."""
    url = request.host_url + 'reset/'
    details = request.get_json()
    email = details['email']
    if not is_valid_email(email):
        return raise_error(400, "Invalid Email Format!")
    user = json.loads(UsersModel().get_user_by_email(email))
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


@portal_v1.route('/students/reset', methods=['POST'])
def reset_user_password():
    """Reset password."""
    """Already existing user can update their password."""
    url = request.host_url + 'reset/'
    details = request.get_json()
    reset_token = details['reset_token']
    password = details['password']
    u_id = decode_token(reset_token)['identity']
    user = json.loads(UsersModel().get_user_by_id(user_id=u_id))
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


@portal_v1.route('/users/refresh', methods=['POST'])
@jwt_refresh_token_required
def user_refresh_token():
    current_user = get_jwt_identity()
    expires = timedelta(days=365)
    access_token = create_access_token(current_user, expires_delta=expires)
    ret = {
        'access_token': access_token
    }
    return jsonify(ret), 200


@portal_v1.route('/users/protected', methods=['GET'])
@jwt_required
def user_protected_route():
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200


@portal_v1.route('/staff/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    """An admin can fetch all users."""
    users = json.loads(UsersModel().get_all_users())
    return make_response(jsonify({
        "status": "200",
        "message": "successfully retrieved",
        "Users": users
    }), 200)


@portal_v1.route('/students/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_student_by_id(user_id):
    """Fetch user by id."""
    user = json.loads(UsersModel().get_user_by_id(user_id))
    if user:
        return make_response(jsonify({
            "status": "200",
            "message": "successfully retrieved",
            "user": user
        }), 200)
    return raise_error(404, "User not found")


@portal_v1.route('/students/users/<string:admission_no>', methods=['GET'])
@jwt_required
def get_user_info(admission_no):
    """An admin can fetch a single user."""
    user = json.loads(UsersModel().get_user_info(admission_no))
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


@portal_v1.route('/students/users/user_info/<string:admission_no>', methods=['PUT'])
@jwt_required
def update_student_info(admission_no):
    """Update user information."""
    errors = check_update_user_keys(request)
    if errors:
        return Serializer.serialize(errors, 400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    surname = details['surname']
    response = UsersModel().update_user_info(
        firstname, lastname, surname, admission_no)
    if response:
        return Serializer.serialize(response, 200, "User updated successfully")
    return Serializer.serialize(response, 404, "User not found")
