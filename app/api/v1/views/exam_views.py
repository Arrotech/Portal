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
    if AcademicYearModel().get_academic_year_by_id(year_id):
        if UsersModel().get_user_by_admission(admission_no):
            if UnitsModel().get_unit_by_name(unit_name):
                response = ExamsModel(year_id, admission_no,
                                      unit_name, marks).save()
                if "error" in response:
                    return raise_error(400, "User does not exist or your are trying to enter marks twice")
                return Serializer.serialize(response, 201, "Marks added successfully")
            return raise_error(404, "Unit {} not found".format(unit_name))
        return raise_error(400, "User does not exist or your are trying to enter marks twice")
    return raise_error(404, "Year not found")


@portal_v1.route('/exams/<string:admission_no>', methods=['GET'])
@jwt_required
def get_exams_for_a_student_by_admission(admission_no):
    """Fetch all exams for a specific student."""
    response = ExamsModel().fetch_all_exams_for_specific_student(admission_no)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")


@portal_v1.route('/exams/year/<string:admission_no>/<string:year>', methods=['GET'])
@jwt_required
def get_all_exams(admission_no, year):
    """Fetch all exams."""
    response = ExamsModel().fetch_all_exams_for_specific_year(admission_no, year)
    return Serializer.serialize(response, 200, "Exams successfull retrieved")
