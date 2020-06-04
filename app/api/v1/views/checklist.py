import json
from flask import request
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from app.api.v1 import checklist_v1
from app.api.v1.models.checklist import ChecklistModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.departments import DepartmentsModel
from app.api.v1.models.courses import CoursesModel
from app.api.v1.models.hostels import HostelsModel
from utils.utils import raise_error, check_checklist_keys
from utils.authorization import admin_required


@checklist_v1.route('/checklist', methods=['POST'])
@jwt_required
def fill_checklist():
    """Fill checklist form."""
    details = request.get_json()
    errors = check_checklist_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    admission_no = details['admission_no']
    department_name = details['department_name']
    course_name = details['course_name']
    hostel_name = details['hostel_name']
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        if DepartmentsModel().get_department_name(department_name):
            if CoursesModel().get_course_name(course_name):
                if HostelsModel().get_hostel_by_name(hostel_name):
                    response = ChecklistModel(admission_no, department_name, course_name, hostel_name).save()
                    if "error" in response:
                        return raise_error(500, "Check your input")
                    return Serializer.serialize(response, 201, "Checklist filled successfully")
                return raise_error(404, "Hostel not found")
            return raise_error(404, "Course not found")
        return raise_error(404, "Department not found")
    return raise_error(404, "User not found")