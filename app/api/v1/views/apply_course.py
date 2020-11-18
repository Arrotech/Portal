import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.apply_course import ApplyCoursesModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.campuses import CampusModel
from app.api.v1.models.certificates import CertificatesModel
from app.api.v1.models.departments import DepartmentsModel
from app.api.v1.models.courses import CoursesModel
from app.api.v1.models.institutions import InstitutionsModel
from utils.utils import check_apply_course_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import portal_v1


@portal_v1.route('/apply_course', methods=['POST'])
@jwt_required
def apply_course():
    """Apply a course."""
    errors = check_apply_course_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    institution_name = details['institution_name']
    campus_id = details['campus_id']
    certificate_id = details['certificate_id']
    department_name = details['department_name']
    course_name = details['course_name']
    if UsersModel().get_admission_no(admission_no):
        if InstitutionsModel().get_institution_name(institution_name):
            if CampusModel().get_campus_by_id(campus_id):
                if CertificatesModel().get_certificate_by_id(certificate_id):
                    if DepartmentsModel().get_department_name(department_name):
                        if CoursesModel().get_course_name(course_name):
                            response = ApplyCoursesModel(
                                admission_no, institution_name, campus_id, certificate_id, department_name, course_name).save()
                            if "error" in response:
                                return raise_error(500, "Check your input and try again")
                            return Serializer.serialize(response, 201, "Course applied successfully")
                        return raise_error(404, "Course not found")
                    return raise_error(404, "Department not found")
                return raise_error(404, "Certificate not found")
            return raise_error(404, "Campus not found")
        return raise_error(404, "Institution not found")


@portal_v1.route('/apply_course/<int:application_id>', methods=['GET'])
@jwt_required
def get_course(application_id):
    """Get course by id."""
    response = ApplyCoursesModel().get_course_by_id(application_id)
    if response:
        return Serializer.serialize(response, 200, "Course retrieved successfully")
    return raise_error(404, "Course not found")
