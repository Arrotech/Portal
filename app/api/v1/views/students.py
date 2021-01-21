from flask import make_response, jsonify, request, render_template, url_for
from flask_jwt_extended import create_access_token, jwt_required,\
    get_jwt_identity, create_refresh_token, jwt_refresh_token_required,\
    fresh_jwt_required, get_raw_jwt
from app.api.v1.models.users_model import UsersModel
from utils.utils import default_decode_token, default_encode_token,\
    generate_url, check_register_keys
from werkzeug.security import check_password_hash, generate_password_hash
from app.api.v1 import portal_v1
from utils.serializer import Serializer
from app.api.v1.services.mail import send_email
from arrotechtools import is_valid_email, is_valid_password, raise_error
from utils.authorization import admin_required
from app.api.v1.forms.forms import PasswordForm
from app import jwtmanager


# A storage engine to save revoked tokens. In production if
# speed is the primary concern, redis is a good bet. If data
# persistence is more important for you, postgres is another
# great option. In this example, we will be using an in memory
# store, just to show you how this might work. For more
# complete examples, check out these:
# https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/redis_blacklist.py
# https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist
blacklist = set()
sr = Serializer


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
                          password).save_student()
    token = default_encode_token(email, salt='email-confirm-key')
    confirm_url = generate_url('portal_v1.confirm_email', token=token)
    send_email.delay('Confirm Your Email',
                     sender='arrotechdesign@gmail.com',
                     recipients=[email],
                     text_body=render_template(
                            'email_confirmation.txt', confirm_url=confirm_url),
                     html_body=render_template('email_confirmation.html',
                                               confirm_url=confirm_url))
    return sr.serialize(response, 201, "Account created successfully!")


# For this example, we are just checking if the tokens jti
# (unique identifier) is in the blacklist set. This could
# be made more complex, for example storing all tokens
# into the blacklist with a revoked status when created,
# and returning the revoked status in this call. This
# would allow you to have a list of all created tokens,
# and to consider tokens that aren't in the blacklist
# (aka tokens you didn't create) as revoked. These are
# just two options, and this can be tailored to whatever
# your application needs.
@jwtmanager.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@portal_v1.route('/students/login', methods=['POST'])
def student_login():
    """Already existing user can sign in to their account."""
    details = request.get_json()
    email = details['email']
    password = details['password']
    user = UsersModel().get_user_by_email(email)
    if user:
        password_db = user['password']
        if check_password_hash(password_db, password):
            token = create_access_token(
                identity=email, fresh=True)
            refresh_token = create_refresh_token(
                identity=email)
            return make_response(jsonify({
                "status": "200",
                "message": "Successfully logged in!",
                "token": token,
                "refresh_token": refresh_token,
                "user": user
            }), 200)
        return raise_error(401, "Invalid Email or Password")
    return raise_error(401, "Invalid Email or Password")


@portal_v1.route('/students/fresh-login', methods=['POST'])
def fresh_student_login():
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


# Endpoint for revoking the current users access token
@portal_v1.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@portal_v1.route('/refresh/logout', methods=['DELETE'])
@jwt_refresh_token_required
def refresh_logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@portal_v1.route('/students/confirm/<token>')
def confirm_email(token):
    """Confirm email."""
    try:
        email = default_decode_token(
            token, salt='email-confirm-key', expiration=3600)
    except Exception:
        return raise_error(404, "User not found")
    user = UsersModel().get_user_by_email(email)
    user_id = user['user_id']
    if user:
        response = UsersModel().confirm_user_email(
            user_id, is_confirmed=True)
        return sr.serialize(response,
                            200,
                            "You have confirmed your email successfully")
    return raise_error(404, "User not found")


@portal_v1.route('/reset', methods=['POST', 'GET'])
def send_reset_email():
    """Send email for password reset link."""
    details = request.get_json()
    email = details['email']
    if not is_valid_email(email):
        return raise_error(400, "Invalid Email Format!")
    user = UsersModel().get_user_by_email(email)
    if user:
        email = user['email']
        firstname = user['firstname']
        token = default_encode_token(email, salt='recover-key')
        recover_url = url_for(
            'portal_v1.reset_with_token', token=token, _external=True)
        send_email('Reset your password',
                   sender='arrotechdesign@gmail.com',
                   recipients=[email],
                   text_body=render_template(
                       'reset_password.txt', recover_url=recover_url,
                       firstname=firstname),
                   html_body=render_template('reset_password.html',
                                             recover_url=recover_url,
                                             firstname=firstname))
        return raise_error(200, "Check Your Email for the Password Reset Link")
    return raise_error(200, "Check Your Email for the Password Reset Link")


@portal_v1.route('/reset/<token>', methods=['POST', 'GET'])
def reset_with_token(token):
    """Reset password."""
    """Already existing user can update their password."""
    try:
        email = default_decode_token(
            token, salt="recover-key", expiration=86400)
    except Exception:
        return raise_error(404, "User not found")
    form = PasswordForm()
    user = UsersModel().get_user_by_email(email)
    if form.validate_on_submit():
        if user:
            email = user['email']
            user_id = user['user_id']
            hashed_password = generate_password_hash(
                password=form.password.data)
            response = UsersModel().update_user_password(hashed_password,
                                                         user_id)
            send_email('Password reset successful',
                       sender='arrotechdesign@gmail.com',
                       recipients=[email],
                       text_body='Password reset was successful',
                       html_body='<p>Password reset was successful</p>')
            return Serializer.serialize(response, 200,
                                        "Password reset successful")
        return raise_error(404, "User not found")
    return render_template('reset_with_token.html', form=form, token=token)


@portal_v1.route('/users/refresh', methods=['POST'])
@jwt_refresh_token_required
def user_refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(current_user, fresh=False)
    ret = {
        'access_token': access_token
    }
    return jsonify(ret), 200


@portal_v1.route('/users/protected', methods=['GET'])
@jwt_required
def user_protected_route():
    email = get_jwt_identity()
    return jsonify(logged_in_as=email), 200


@portal_v1.route('/users/fresh-protected', methods=['GET'])
@fresh_jwt_required
def protected_fresh():
    email = get_jwt_identity()
    return jsonify(fresh_logged_in_as=email), 200


@portal_v1.route('/students/users/<int:user_id>', methods=['GET'])
@jwt_required
def get_student_by_id(user_id):
    """Fetch user by id."""
    user = UsersModel().get_user_by_id(user_id)
    if user:
        return Serializer.serialize(user, 200, "successfully retrieved")
    return raise_error(404, "User not found")


@portal_v1.route('/students/users/<string:admission_no>', methods=['GET'])
@jwt_required
def get_user_info(admission_no):
    """An admin can fetch a single user."""
    user = UsersModel().get_user_info(admission_no)
    if user:
        return Serializer.serialize(user, 200, "successfully retrieved")
    return raise_error(404, "User Not Found")
