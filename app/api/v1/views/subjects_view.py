from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.subject_model import SubjectsModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from app.api.v1.models.academic_year import AcademicYearModel
from utils.utils import check_subjects_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import portal_v1


@portal_v1.route('/subjects', methods=['POST'])
@jwt_required
def register_subjects():
    """Register a subject."""
    errors = check_subjects_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    unit_name = details['unit_name']
    year_id = details['year_id']
    if UsersModel().get_user_by_admission(admission_no):
        if UnitsModel().get_unit_by_name(unit_name):
            if AcademicYearModel().get_academic_year_by_id(year_id):
                response = SubjectsModel(admission_no,
                                         unit_name,
                                         year_id).save()
                return Serializer.serialize(
                    response,
                    201,
                    "You have successfully registered {}".format(unit_name))
            return raise_error(404, "Year not found")
        return raise_error(404, "Unit {} not found".format(unit_name))
    return raise_error(404, "User not found")


@portal_v1.route('/subjects', methods=['GET'])
@jwt_required
@admin_required
def get_subjects():
    """Fetch all subjects."""
    response = SubjectsModel().get_subjects()
    return Serializer.serialize(response, 200,
                                "Subjects successfull retrieved")


@portal_v1.route('/subjects/<int:subject_id>', methods=['GET'])
@jwt_required
@admin_required
def get_subject_by_id(subject_id):
    """Fetch subject by id."""
    response = SubjectsModel().get_subject_by_id(subject_id)
    if response:
        return Serializer.serialize(response, 200,
                                    "Subject successfull retrieved")
    return raise_error(404, "Subject not found")


@portal_v1.route('/subjects/<string:admission_no>', methods=['GET'])
@jwt_required
def get_subjects_for_specific_user_by_admission(admission_no):
    """Fetch all subjects for a specific user by admission."""
    response = SubjectsModel().\
        get_subjects_for_specific_user_by_admission(admission_no)
    return Serializer.serialize(response, 200,
                                "Subjects successfull retrieved")


@portal_v1.route('/subjects/total/<string:admission_no>', methods=['GET'])
@jwt_required
def get_total_number_of_registered_units_by_admission(admission_no):
    """Fetch the total number of registered units for a specific student."""
    response = SubjectsModel().\
        get_total_number_of_registered_units_by_admission(admission_no)
    return Serializer.serialize(response, 200,
                                "Total registered units")


@portal_v1.route('/subjects/total/year/<string:admission_no>', methods=['GET'])
@jwt_required
def get_total_number_of_registered_units_by_admission_and_year(admission_no):
    """Fetch the total number of registered units for a specific year."""
    response = SubjectsModel().\
        get_total_number_of_registered_units_by_admission_and_year(
            admission_no)
    return Serializer.serialize(response, 200,
                                "Total registered units")


@portal_v1.route('/subjects/<string:admission_no>/<string:year>',
                 methods=['GET'])
@jwt_required
def get_subjects_for_specific_user_by_year(admission_no, year):
    """Fetch all subjects for a specific user for specific year."""
    response = SubjectsModel().\
        get_subjects_for_specific_user_by_year(
        admission_no,
        year)
    return Serializer.serialize(response, 200,
                                "Subjects successfull retrieved")


@portal_v1.route(
    '/subjects/<string:admission_no>/<string:year>/<string:semester>',
    methods=['GET'])
@jwt_required
def get_subjects_for_specific_user_by_semester(admission_no, year, semester):
    """Fetch all subjects for a specific user for specific semester."""
    response = SubjectsModel().get_subjects_for_specific_user_by_semester(
        admission_no, year, semester)
    return Serializer.serialize(response, 200,
                                "Subjects successfull retrieved")


@portal_v1.route('/subjects/<int:subject_id>', methods=['PUT'])
@jwt_required
def update_subject_by_id(subject_id):
    """Update subject by id."""
    details = request.get_json()
    unit_name = details['unit_name']
    response = SubjectsModel().edit_subject_by_id(unit_name, subject_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Subject updated successfully')
    return raise_error(404, "Subject not found")


@portal_v1.route('/subjects/<int:subject_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_subject(subject_id):
    """Delete a subject by id."""
    response = SubjectsModel().get_subject_by_id(subject_id)
    if response:
        SubjectsModel().delete(subject_id)
        return Serializer.serialize(response, 200,
                                    "Subject deleted successfully")
    return raise_error(404, "Subject not found")
