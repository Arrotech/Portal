import json
import os
from datetime import datetime, timedelta
from flask import make_response, jsonify, request, Blueprint, render_template, url_for, redirect
from flask_jwt_extended import decode_token, create_access_token, jwt_required, get_jwt_identity, create_refresh_token, jwt_refresh_token_required, get_raw_jwt
from app.api.v1.models.users_model import UsersModel
from utils.utils import default_decode_token, default_encode_token, generate_url, check_update_user_keys, check_register_keys, form_restrictions, check_promote_student_keys
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from itsdangerous import URLSafeTimedSerializer
from app.api.v1.services.mails.mail_services import send_email
from arrotechtools import is_valid_email, is_valid_password, raise_error
from utils.authorization import admin_required, registrar_required
from app.api.v1.forms.forms import EmailForm, PasswordForm


@portal_v1.route('/library/register', methods=['POST', 'GET'])
@jwt_required
@registrar_required
def librarian_signup():
    """The registrar can add a new librarian."""
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
    user_admission = UsersModel().get_user_by_admission(admission_no)
    if user_admission:
        return raise_error(400, "Admission number Already Exists!")
    user_email = UsersModel().get_user_by_email(email)
    if user_email:
        return raise_error(400, "Email Already Exists!")
    response = UsersModel(firstname, lastname, surname,
                          admission_no, gender, email, password).save_librarian()
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
    send_email.delay('Confirm Your Email',
                     sender='arrotechdesign@gmail.com',
                     recipients=[email],
                     text_body=render_template(
                            'email_confirmation.txt', confirm_url=confirm_url),
                     html_body=render_template('email_confirmation.html', confirm_url=confirm_url))
    return Serializer.serialize(response, 201, "Account created successfully!")