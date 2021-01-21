import os
from datetime import timedelta
from flask import make_response, jsonify, request, render_template, url_for,\
    session, redirect
from flask_jwt_extended import create_access_token, jwt_required,\
    create_refresh_token
from app.api.v1.models.users_model import UsersModel
from utils.utils import default_encode_token, generate_url,\
    check_update_user_keys, check_register_keys
from werkzeug.security import check_password_hash
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from app.api.v1.services.mail import send_email
from arrotechtools import is_valid_email, is_valid_password, raise_error
from utils.authorization import admin_required, registrar_required
from flask_oauth import OAuth

oauth = OAuth()
google = oauth.remote_app(
    'google',
    base_url='https://www.google.com/accounts/',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    request_token_url=None,
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'response_type': 'code'},
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_method='POST',
    access_token_params={
        'grant_type': 'authorization_code'},
    consumer_key=os.environ.get('GOOGLE_CLIENT_ID'),
    consumer_secret=os.environ.get('GOOGLE_CLIENT_SECRET'))


@portal_v1.route('/staff/register', methods=['POST', 'GET'])
@jwt_required
@registrar_required
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
        return raise_error(400, "Invalid password")
    user_admission = UsersModel().get_user_by_admission(admission_no)
    if user_admission:
        return raise_error(400, "Admission number Already Exists!")
    user_email = UsersModel().get_user_by_email(email)
    if user_email:
        return raise_error(400, "Email Already Exists!")
    response = UsersModel(firstname,
                          lastname,
                          surname,
                          admission_no,
                          gender,
                          email,
                          password).save_admin()
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
    send_email.delay('Confirm Your Email',
                     sender='arrotechdesign@gmail.com',
                     recipients=[email],
                     text_body=render_template(
                            'email_confirmation.txt', confirm_url=confirm_url),
                     html_body=render_template('email_confirmation.html',
                                               confirm_url=confirm_url))
    return Serializer.serialize(response, 201, "Account created successfully!")


@portal_v1.route('/staff/login', methods=['POST'])
def staff_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = UsersModel().get_user_by_email(email)
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            expires = timedelta(days=365)
            token = create_access_token(
                identity=email, expires_delta=expires)
            refresh_token = create_refresh_token(
                identity=email, expires_delta=expires)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "token": token,
                "refresh_token": refresh_token,
                "user": user
            }), 200)
        return raise_error(401, "Invalid Email or Password")
    return raise_error(401, "Invalid Email or Password")


@portal_v1.route('/staff/fresh-login', methods=['POST'])
def fresh_staff_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = UsersModel().get_user_by_email(email)
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            access_token = create_access_token(
                identity=email, fresh=True)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "access_token": access_token,
                "user": user
            }), 200)
        return raise_error(401, "Invalid Email or Password")
    return raise_error(401, "Invalid Email or Password")


@portal_v1.route('/google/login')
def google_login():
    callback = url_for('portal_v1.authorized', _external=True)
    return google.authorize(callback=callback)


@portal_v1.route("/callback")
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('/'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


@portal_v1.route('/staff/users', methods=['GET'])
@jwt_required
@admin_required
def get_all_users():
    """An admin can fetch all users."""
    users = UsersModel().get_all_users()
    return Serializer.serialize(users, 200, "successfully retrieved")


@portal_v1.route('/staff/users/<string:role>', methods=['GET'])
@jwt_required
@admin_required
def get_grouped_users(role):
    users = UsersModel().get_grouped_users(role)
    return Serializer.serialize(users, 200, "successfully retrieved")


@portal_v1.route('/staff/students/<string:role>', methods=['GET'])
@jwt_required
@admin_required
def get_students_total(role):
    users = UsersModel().number_of_users(role)
    return Serializer.serialize(users, 200, "successfully retrieved")


@portal_v1.route('/user/update/<string:admission_no>', methods=['PUT'])
@jwt_required
@admin_required
def update_user_info(admission_no):
    """Update user information."""
    errors = check_update_user_keys(request)
    if errors:
        return Serializer.serialize(errors, 400,
                                    'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    firstname = details['firstname']
    lastname = details['lastname']
    surname = details['surname']
    gender = details['gender']
    response = UsersModel().update_user_info(
        firstname, lastname, surname, gender, admission_no)
    if response:
        return Serializer.serialize(response, 200, "User updated successfully")
    return Serializer.serialize(response, 404, "User not found")
