from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import exams_v1
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from app.api.v1.models.exams_model import ExamsModel
from utils.utils import check_exams_keys, raise_error
from utils.serializer import Serializer


@exams_v1.route('/exams', methods=['POST'])
@jwt_required
def add_exam():
    """Make a new exam entry."""
    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    user_id = details['user_id']
    unit_id = details['unit_id']
    marks = details['marks']
    if UsersModel().get_user_id(user_id):
        if UnitsModel().get_unit_by_id(unit_id):
            response = ExamsModel(user_id, unit_id, marks).save()
            if "error" in response:
                return raise_error(400, "User does not exist or your are trying to enter marks twice")
            return Serializer.serialize(response, 201, "You have successfully added {}".format(marks))
        return raise_error(404, "Unit {} not found".format(unit_id))
    return raise_error(404, "Student {} not found".format(user_id))
