import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.institutions import InstitutionsModel
from utils.utils import check_institutions_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import institutions_v1


@institutions_v1.route('/institutions', methods=['POST'])
@jwt_required
@admin_required
def add_institution():
    """Add new institution."""
    errors = check_institutions_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    institution_name = details['institution_name']
    response = InstitutionsModel(institution_name).save()
    return Serializer.serialize(response, 201, "Institution added successfully")

@institutions_v1.route('/institutions', methods=['GET'])
@jwt_required
def get_all_institutions():
    """Fetch all institutions."""
    response = InstitutionsModel().get_all_institutions()
    return Serializer.serialize(response, 200, "Institutions retrieved successfully")

@institutions_v1.route('/institutions/<int:institution_id>', methods=['GET'])
@jwt_required
@admin_required
def get_institution_by_id(institution_id):
    """Fetch institution by id."""
    response = InstitutionsModel().get_institution_by_id(institution_id)
    if response:
        return Serializer.serialize(response, 200, "Institution retrieved successfully")
    return raise_error(404, "Institution not found")

@institutions_v1.route('/institutions/<int:institution_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_institution(institution_id):
    """Delete institution by id."""
    if InstitutionsModel().get_institution_by_id(institution_id):
        response = InstitutionsModel().delete(institution_id)
        return Serializer.serialize(response, 200, "Institution deleted successfully")
    return raise_error(404, 'Institution not found')