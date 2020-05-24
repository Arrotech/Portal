from flask import request
from flask_jwt_extended import jwt_required
from app.api.v1 import exams_v1
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.units import UnitsModel
from app.api.v1.models.exams_model import ExamsModel
from utils.utils import check_exams_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required


@exams_v1.route('/exams', methods=['POST'])
@jwt_required
def add_exam():
    """Make a new exam entry."""
    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    semester = details['semester']
    year = details['year']
    admission_no = details['admission_no']
    unit_name = details['unit_name']
    marks = details['marks']
    if UsersModel().get_user_by_admission(admission_no):
        if UnitsModel().get_unit_by_name(unit_name):
            response = ExamsModel(semester, year, admission_no,
                                  unit_name, marks).save()
            if "error" in response:
                return raise_error(400, "User does not exist or your are trying to enter marks twice")
            return Serializer.serialize(response, 201, "Marks added successfully")
        return raise_error(404, "Unit {} not found".format(unit_name))


@exams_v1.route('/exams', methods=['GET'])
@jwt_required
@admin_required
def get_exams():
    """Fetch all exams."""
    response = ExamsModel().get_exams()
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@exams_v1.route('/exams/<string:admission_no>', methods=['GET'])
@jwt_required
def get_exams_for_a_student(admission_no):
    """Fetch all exams for a specific student."""
    response = ExamsModel().get_exams_for_a_student_by_admission(admission_no)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")
