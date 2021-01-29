from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import portal_v1
from app.api.v1.models.academic_year import AcademicYearModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from app.api.v1.models.exams_model import ExamsModel
from utils.utils import check_exams_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required


@portal_v1.route('/exams', methods=['POST'])
@jwt_required
@admin_required
def add_exam():
    """Make a new exam entry."""
    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    year_id = details['year_id']
    admission_no = details['admission_no']
    unit_name = details['unit_name']
    marks = details['marks']
    exam_type = details['exam_type']
    if AcademicYearModel().get_academic_year_by_id(year_id):
        if UsersModel().get_user_by_admission(admission_no):
            if UnitsModel().get_unit_by_name(unit_name):
                response = ExamsModel(year_id, admission_no,
                                      unit_name, marks, exam_type).save()
                return Serializer.serialize(response,
                                            201,
                                            "Marks added successfully")
            return raise_error(404, "Unit {} not found".format(unit_name))
        return raise_error(
            400,
            "User does not exist or your are trying to enter marks twice")
    return raise_error(404, "Year not found")


@portal_v1.route('/exams/<string:admission_no>', methods=['GET'])
@jwt_required
def get_all_exams_for_a_student_by_admission(admission_no):
    """Fetch all exams for a specific student."""
    response = ExamsModel().fetch_all_exams_for_specific_student(admission_no)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@portal_v1.route('/exams/aggregate/<string:admission_no>/<string:year>',
                 methods=['GET'])
@jwt_required
def get_aggregated_points(admission_no, year):
    """Get average marks."""
    print("@@@@@@@@@@@@@@@@@@@@@@_-------")
    response = ExamsModel().fetch_aggregated_points(admission_no, year)
    return Serializer.serialize(response, 200,
                                "Exam Total successfull retrieved")


@portal_v1.route('/exams/<int:exam_id>', methods=['GET'])
@jwt_required
@admin_required
def get_exam_by_id(exam_id):
    """Fetch an exam by Id."""
    response = ExamsModel().fetch_exam_by_id(exam_id)
    return Serializer.serialize(response, 200, "Exam successfull retrieved")


@portal_v1.route('/exams/year/<string:admission_no>/<string:year>',
                 methods=['GET'])
@jwt_required
def get_exams_for_specific_year(admission_no, year):
    """Fetch all exams."""
    response = ExamsModel().fetch_all_exams_for_specific_year(admission_no,
                                                              year)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@portal_v1.route(
    '/exams/year/<string:admission_no>/<string:year>/<string:semester>',
    methods=['GET'])
@jwt_required
def get_exams_for_specific_semester(admission_no, year, semester):
    """Fetch all exams fro specific semester."""
    response = ExamsModel().fetch_all_exams_for_specific_semester(
        admission_no, year, semester)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@portal_v1.route('/exams/total/<string:admission_no>/<string:unit>',
                 methods=['GET'])
@jwt_required
def get_total_for_specific_unit(admission_no, unit):
    """Fetch all exams fro specific semester."""
    response = ExamsModel().fetch_total_for_specific_unit(admission_no, unit)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@portal_v1.route('/exams/<int:exam_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_exam_by_id(exam_id):
    """Update exam by id."""
    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    year_id = details['year_id']
    admission_no = details['admission_no']
    unit_name = details['unit_name']
    marks = details['marks']
    response = ExamsModel().update(year_id, admission_no,
                                   unit_name, marks, exam_id)
    if response:
        return Serializer.serialize(response, 200, 'Exam updated successfully')
    return raise_error(404, "Exam not found")


@portal_v1.route('/exams/<int:exam_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_exam(exam_id):
    """Delete exam by id."""
    response = ExamsModel().fetch_exam_by_id(exam_id)
    if response:
        ExamsModel().delete(exam_id)
        return Serializer.serialize(response, 200, "Exam deleted successfully")
    return raise_error(404, 'Exam not found')
