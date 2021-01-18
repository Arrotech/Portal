from flask import request, render_template
from flask_jwt_extended import jwt_required
from app.api.v1.models.users_model import UsersModel
from utils.utils import default_encode_token, generate_url,\
    check_register_keys
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from app.api.v1.services.mail import send_email
from arrotechtools import is_valid_email, is_valid_password, raise_error
from utils.authorization import registrar_required


@portal_v1.route('/department/register', methods=['POST', 'GET'])
@jwt_required
@registrar_required
def department_head_signup():
    """The registrar can add a new department head."""
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
                          password).save_department_head()
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
