from flask import make_response, jsonify, request, render_template
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required,\
    create_refresh_token
from app.api.v1.models.users_model import UsersModel
from utils.utils import default_encode_token, generate_url, check_register_keys
from werkzeug.security import check_password_hash
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from app.api.v1.services.mail import send_email
from arrotechtools import is_valid_email, is_valid_password, raise_error
from utils.authorization import registrar_required


@portal_v1.route('/accountant/register', methods=['POST', 'GET'])
@jwt_required
@registrar_required
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
                          password).save_accountant()
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


@portal_v1.route('/accountant/login', methods=['POST'])
def accountant_login():
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
