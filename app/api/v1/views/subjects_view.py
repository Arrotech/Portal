import json

from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.subject_model import SubjectsModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from utils.utils import check_subjects_keys, raise_error
from utils.serializer import Serializer

subjects_v1 = Blueprint('subjects_v1', __name__)


@subjects_v1.route('/subjects', methods=['POST'])
@jwt_required
def register_subjects():
    """Register a subject."""
    errors = check_subjects_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    user_id = details['user_id']
    unit_id = details['unit_id']
    if UsersModel().get_user_id(user_id):
        if UnitsModel().get_unit_by_id(unit_id):
            response = SubjectsModel(user_id,unit_id).save()
            if "error" in response:
                return raise_error(400, "You cannot register for one unit twice")
            return Serializer.serialize(response, 201, "You have successfully registered {}".format(unit_id))
        return raise_error(404, "Unit {} not found".format(unit_id))
    return raise_error(404, "Student {} not found".format(user_id))