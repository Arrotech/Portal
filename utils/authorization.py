import json
from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.api.v1.models.users_model import UsersModel
from utils.serializer import Serializer


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
