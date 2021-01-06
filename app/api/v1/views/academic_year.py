import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.academic_year import AcademicYearModel
from utils.utils import check_year_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import registrar_required
from app.api.v1 import portal_v1


@portal_v1.route('/year', methods=['POST'])
@jwt_required
@registrar_required
def add_year():
    """Add new academic year."""
    errors = check_year_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    year = details['year']
    semester = details['semester']
    response = AcademicYearModel(year, semester).save()
    return Serializer.serialize(response, 201, "Year added successfully")


@portal_v1.route('/year', methods=['GET'])
@jwt_required
def get_all_academic_years():
    """Get all academic years."""
    response = AcademicYearModel().get_all_academic_years()
    return Serializer.serialize(response, 200, "Years retrieved successfully")


@portal_v1.route('/year/<int:year_id>', methods=['GET'])
@jwt_required
def get_year_by_id(year_id):
    """Get specific academic year by id."""
    response = AcademicYearModel().get_academic_year_by_id(year_id)
    if response:
        return Serializer.serialize(response, 200, "Year retrieved successfully")
    return raise_error(404, "Year not found")


@portal_v1.route('/year/<int:year_id>', methods=['PUT'])
@jwt_required
@registrar_required
def update_year(year_id):
    """Update specific year by id."""
    details = request.get_json()
    errors = check_year_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    year = details['year']
    semester = details['semester']
    response = AcademicYearModel().edit_academic_year(year, semester, year_id)
    if response:
        return Serializer.serialize(response, 200, 'Year updated successfully')
    return raise_error(404, "Year not found")


@portal_v1.route('/year/<int:year_id>', methods=['DELETE'])
@jwt_required
@registrar_required
def delete_academic_year(year_id):
    """Delete specific academic year by id."""
    response = AcademicYearModel().get_academic_year_by_id(year_id)
    if response:
        AcademicYearModel().delete(year_id)
        return Serializer.serialize(response, 200, "Year deleted successfully")
    return raise_error(404, 'Year not found')
