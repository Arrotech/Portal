import json
from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.api.v1.models.users_model import UsersModel


def bursar_required(func):
    """ Admin Rights."""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = UsersModel().get_users()
        users = json.loads(users)
        try:
            cur_user = [
                user for user in users if user['email'] == get_jwt_identity()]
            user_role = cur_user[0]['role']
            if user_role != 'bursar':
                return {
                        'message': 'This activity can be completed by bursar only'}, 403  # Forbidden
            return func(*args, **kwargs)
        except Exception as e:
            return {"message": e}

    return wrapper_function