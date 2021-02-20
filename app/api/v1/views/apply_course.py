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
from utils.authorization import registrar_required
from app.api.v1 import portal_v1


sr = Serializer


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
    if UsersModel().get_user_by_admission(admission_no):
        if InstitutionsModel().get_institution_name(institution_name):
            if CampusModel().get_campus_by_id(campus_id):
                if CertificatesModel().get_certificate_by_id(certificate_id):
                    if DepartmentsModel().get_department_name(department_name):
                        if CoursesModel().get_course_name(course_name):
                            response = ApplyCoursesModel(admission_no,
                                                         institution_name,
                                                         campus_id,
                                                         certificate_id,
                                                         department_name,
                                                         course_name).save()
                            return sr.serialize(response,
                                                201,
                                                "Course applied successfully")
                        return raise_error(404, "Course not found")
                    return raise_error(404, "Department not found")
                return raise_error(404, "Certificate not found")
            return raise_error(404, "Campus not found")
        return raise_error(404, "Institution not found")
    return raise_error(404, "Student not found")


@portal_v1.route('/apply_course', methods=['GET'])
@jwt_required
@registrar_required
def get_all_applied_courses():
    """Fetch all applied courses."""
    response = ApplyCoursesModel().get_all_applied_courses()
    return sr.serialize(response, 200,
                        "Applied courses retrieved successfully")


@portal_v1.route('/apply_course/total/<string:course>', methods=['GET'])
@jwt_required
def get_total_number_of_students_per_course(course):
    """Fetch the total number of students per course."""
    response = ApplyCoursesModel().get_total_number_of_students_per_course(course)
    return sr.serialize(response, 200,
                        "Total number of students retrieved successfully")


@portal_v1.route('/apply_course/<int:application_id>', methods=['GET'])
@jwt_required
def get_applied_course_by_id(application_id):
    """Get course by id."""
    response = ApplyCoursesModel().get_course_by_id(application_id)
    if response:
        return sr.serialize(response, 200,
                            "Course retrieved successfully")
    return raise_error(404, "Course not found")


@portal_v1.route('/apply_course/<string:admission_no>', methods=['GET'])
@jwt_required
def get_course_info(admission_no):
    """Get course by admission_no."""
    res = ApplyCoursesModel().get_course_info_by_admission_no(admission_no)
    if res:
        return sr.serialize(res, 200,
                            "Course retrieved successfully")
    return raise_error(404, "Course not found")


@portal_v1.route('/apply_course/<int:application_id>', methods=['PUT'])
@jwt_required
def update_applied_course(application_id):
    """Update applied course by id."""
    details = request.get_json()
    institution_name = details['institution_name']
    campus_id = details['campus_id']
    certificate_id = details['certificate_id']
    department_name = details['department_name']
    course_name = details['course_name']
    response = ApplyCoursesModel().update(institution_name,
                                          campus_id,
                                          certificate_id,
                                          department_name,
                                          course_name,
                                          application_id)
    if response:
        return sr.serialize(response, 200,
                            'Applied course updated successfully')
    return raise_error(404, "Applied course not found")


@portal_v1.route('/apply_course/<int:application_id>', methods=['DELETE'])
@jwt_required
def delete__applied_course(application_id):
    """Delete applied course by id."""
    response = ApplyCoursesModel().get_course_by_id(application_id)
    if response:
        ApplyCoursesModel().delete(application_id)
        return sr.serialize(response, 200,
                            "Applied course deleted successfully")
    return raise_error(404, 'Applied course not found')
