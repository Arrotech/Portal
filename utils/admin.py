import json
from functools import wraps

from flask_jwt_extended import get_jwt_identity

# from app.api.v1.models.staff import StaffModel

def admin_required(users_dict):

    def admin_role(func):
        """ Admin Rights."""

        @wraps(func)
        def wrapper_function(*args, **kwargs):
            # users = StaffModel().get_users()
            # users = json.loads(users)
            try:
                cur_user = [
                    user for user in users_dict if user['email'] == get_jwt_identity()]
                user_role = cur_user[0]['role']
                if user_role != 'teacher':
                    return {
                        'message': 'This activity can only be completed by the class teacher'}, 403  # Forbidden
                return func(*args, **kwargs)
            except Exception as e:
                return {"message": e}

        return wrapper_function
    return admin_role
