from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.api.v1.models.users_model import UsersModel
from utils.serializer import Serializer


def registrar_required(func):
    """ Registrar Rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            users = UsersModel().get_all_users()
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'registrar':
                return {
                    'message': 'This activity can only be completed by the registrar'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return Serializer.serialize("{}".format(e), 500, "Error")

    return wrapper_function


def college_head(func):
    """ College Head Rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            users = UsersModel().get_all_users()
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'college':
                return {
                    'message': 'This activity can only be completed by the college head'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return Serializer.serialize("{}".format(e), 500, "Error")

    return wrapper_function


def department_head(func):
    """ Department Head Rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            users = UsersModel().get_all_users()
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'department':
                return {
                    'message': 'This activity can only be completed by the dean of department'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return Serializer.serialize("{}".format(e), 500, "Error")

    return wrapper_function


def admin_required(func):
    """ Admin Rights."""
    @wraps(func)
    def wrapper_function(*args, **kwargs):
        try:
            users = UsersModel().get_all_users()
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'admin':
                return {
                    'message': 'This activity can only be completed by the admin'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return Serializer.serialize("{}".format(e), 500, "Error")

    return wrapper_function


def accountant_required(func):
    """ Accountant Rights."""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = UsersModel().get_all_users()
        try:
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'accountant':
                return {
                    'message': 'This activity can only be completed by the accountant'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}

    return wrapper_function


def hostel_manager(func):
    """ Hostel Manager Rights."""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = UsersModel().get_all_users()
        try:
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'hostel':
                return {
                    'message': 'This activity can only be completed by the hostel manager'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}

    return wrapper_function


def librarian_required(func):
    """ Library Manager Rights."""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = UsersModel().get_all_users()
        try:
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'librarian':
                return {
                    'message': 'This activity can only be completed by the library manager'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}

    return wrapper_function
