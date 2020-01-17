import json
from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.api.v1.models.accountant import AccountantModel


def accountant_required(func):
    """ Admin Rights."""

    @wraps(func)
    def wrapper_function(*args, **kwargs):
        users = AccountantModel().get_users()
        users = json.loads(users)
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