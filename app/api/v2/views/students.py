from flask import request, render_template, jsonify
from app.api.v2 import portal_v2
from flask_jwt_extended import jwt_required
from utils.authorization import admin_required
from utils.utils import check_register_keys, raise_error, is_valid_email,\
    is_valid_password, default_encode_token, generate_url
from app.api.v2.models.students import User
from app.api.v2.services.mail import send_email
from app.__init__ import db


@portal_v2.route('/students/register', methods=['POST', 'GET'])
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
        return raise_error(400, "Invalid Password!")
    user_admission = User.query.filter_by(admission_no=admission_no).first()
    if user_admission:
        return raise_error(400, "Admission number Already Exists!")
    user_email = User.query.filter_by(email=email).first()
    if user_email:
        return raise_error(400, "Email Already Exists!")
    response = User(firstname, lastname, surname,
                    admission_no, gender, email, password)
    db.session.add(response)
    db.session.commit()
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
    send_email.delay('Confirm Your Email',
                     sender='arrotechdesign@gmail.com',
                     recipients=[email],
                     text_body=render_template(
                            'email_confirmation.txt', confirm_url=confirm_url),
                     html_body=render_template('email_confirmation.html',
                                               confirm_url=confirm_url))

    return jsonify({
        "user": response.as_dict(),
        "message": "Account created successfully!"
    }), 201
