from flask import request
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from app.api.v1 import portal_v1
from app.api.v1.models.checklist import ChecklistModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.departments import DepartmentsModel
from app.api.v1.models.courses import CoursesModel
from app.api.v1.models.certificates import CertificatesModel
from app.api.v1.models.academic_year import AcademicYearModel
from app.api.v1.models.campuses import CampusModel
from app.api.v1.models.hostels import HostelsModel
from utils.utils import raise_error, check_checklist_keys
from utils.authorization import registrar_required


sr = Serializer


@portal_v1.route('/checklist', methods=['POST'])
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
    certificate_id = details['certificate_id']
    year_id = details['year_id']
    campus_id = details['campus_id']
    hostel_name = details['hostel_name']
    user = UsersModel().get_user_by_admission(admission_no)
    if user:
        if DepartmentsModel().get_department_name(department_name):
            if CoursesModel().get_course_name(course_name):
                if CertificatesModel().get_certificate_by_id(certificate_id):
                    if AcademicYearModel().get_academic_year_by_id(year_id):
                        if CampusModel().get_campus_by_id(campus_id):
                            if HostelsModel().get_hostel_by_name(hostel_name):
                                response = ChecklistModel(admission_no,
                                                          department_name,
                                                          course_name,
                                                          certificate_id,
                                                          year_id,
                                                          campus_id,
                                                          hostel_name).save()
                                return sr.serialize(
                                    response,
                                    201,
                                    "Checklist filled successfully")
                            return raise_error(404, "Hostel not found")
                        return raise_error(404, "Campus not found")
                    return raise_error(404, "Year not found")
                return raise_error(404, "Certificate not found")
            return raise_error(404, "Course not found")
        return raise_error(404, "Department not found")
    return raise_error(404, "User not found")


@portal_v1.route('/checklist', methods=['GET'])
@jwt_required
@registrar_required
def get_all_forms():
    """Fetch all applied courses."""
    response = ChecklistModel().get_all_forms()
    return Serializer.serialize(response, 200,
                                "Checklist forms retrieved successfully")


@portal_v1.route('/checklist/<int:checklist_id>', methods=['GET'])
@jwt_required
def get_form_by_id(checklist_id):
    """Get checklist form by id."""
    response = ChecklistModel().get_form_by_id(checklist_id)
    if response:
        return Serializer.serialize(response, 200,
                                    "Checlist form retrieved successfully")
    return raise_error(404, "Checklist form not found")


@portal_v1.route('/checklist/<string:admission_no>', methods=['GET'])
@jwt_required
def get_form_by_admission_no(admission_no):
    """Get checklist form by admission number."""
    response = ChecklistModel().get_form_by_admission_no(admission_no)
    if response:
        return Serializer.serialize(response, 200,
                                    "Checklist form retrieved successfully")
    return raise_error(404, "Checklist form not found")


@portal_v1.route('/checklist/all/<string:admission_no>', methods=['GET'])
@jwt_required
def get_checklist_history_by_admission_no(admission_no):
    """Fetch checklist history by admission number."""
    res = ChecklistModel().get_checklist_history_by_admission_no(admission_no)
    return Serializer.serialize(res, 200,
                                "Checklist forms retrieved successfully")


@portal_v1.route('/checklist/<int:checklist_id>', methods=['PUT'])
@jwt_required
def update_checklist_form(checklist_id):
    """Update checklist by id."""
    details = request.get_json()
    department_name = details['department_name']
    course_name = details['course_name']
    certificate_id = details['certificate_id']
    year_id = details['year_id']
    campus_id = details['campus_id']
    hostel_name = details['hostel_name']
    response = ChecklistModel().update(department_name,
                                       course_name,
                                       certificate_id,
                                       year_id,
                                       campus_id,
                                       hostel_name,
                                       checklist_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Checklist updated successfully')
    return raise_error(404, "Checklist not found")


@portal_v1.route('/checklist/<int:checklist_id>', methods=['DELETE'])
@jwt_required
@registrar_required
def delete__checklist_form(checklist_id):
    """Delete checklist by id."""
    response = ChecklistModel().get_form_by_id(checklist_id)
    if response:
        ChecklistModel().delete(checklist_id)
        return Serializer.serialize(response, 200,
                                    "Checklist deleted successfully")
    return raise_error(404, 'Checklist not found')
