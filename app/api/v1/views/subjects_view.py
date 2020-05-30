import json

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.subject_model import SubjectsModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from utils.utils import check_subjects_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import subjects_v1


@subjects_v1.route('/subjects', methods=['POST'])
@jwt_required
def register_subjects():
    """Register a subject."""
    errors = check_subjects_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    unit_name = details['unit_name']
    if UsersModel().get_user_by_admission(admission_no):
        if UnitsModel().get_unit_by_name(unit_name):
            response = SubjectsModel(admission_no, unit_name).save()
            if "error" in response:
                return raise_error(400, "User does not exist or your are trying to enter marks twice")
            return Serializer.serialize(response, 201, "You have successfully registered {}".format(unit_name))
        return raise_error(404, "Unit {} not found".format(unit_name))


@subjects_v1.route('/subjects', methods=['GET'])
@jwt_required
@admin_required
def get_subjects():
    """Fetch all subjects."""
    response = SubjectsModel().get_subjects()
    return Serializer.serialize(response, 200, "Subjects successfull retrieved")


@subjects_v1.route('/subjects/<string:admission_no>', methods=['GET'])
@jwt_required
def get_subjects_for_specific_user_by_admission(admission_no):
    """Fetch all subjects for a specific user by admission."""
    response = SubjectsModel().get_subjects_for_specific_user_by_admission(admission_no)
    return Serializer.serialize(response, 200, "Subjects successfull retrieved")


@subjects_v1.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_subject(subject_id):
    """Delete a subject by id."""
    response = SubjectsModel().get_subject_by_id(subject_id)
    if response:
        SubjectsModel().delete(subject_id)
        return Serializer.serialize(response, 200, "Subject deleted successfully")
    return raise_error(404, "Subject not found")
