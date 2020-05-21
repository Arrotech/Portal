import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.apply_course import ApplyCoursesModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.departments import DepartmentsModel
from app.api.v1.models.courses import CoursesModel
from utils.utils import check_apply_course_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import apply_course_v1


@apply_course_v1.route('/apply_course', methods=['POST'])
@jwt_required
def apply_course():
    """Apply a course."""
    errors = check_apply_course_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    user_id = details['user_id']
    department_id = details['department_id']
    course_id = details['course_id']
    if UsersModel().get_user_id(user_id):
        if DepartmentsModel().get_department_by_id(department_id):
            if CoursesModel().get_course_by_id(course_id):
                response = ApplyCoursesModel(user_id, department_id, course_id).save()
                if "error" in response:
                    return raise_error(404, "User not found")
                return Serializer.serialize(response, 201, "Course applied successfully")
            return raise_error(404, "Course not found")
        return raise_error(404, "Department not found")
    return raise_error(404, "Student not found")

@apply_course_v1.route('/apply_course/<int:application_id>', methods=['GET'])
@jwt_required
def get_course(application_id):
    """Get course by id."""
    response = ApplyCoursesModel().get_course_by_id(application_id)
    if response:
        return Serializer.serialize(response, 200, "Course retrieved successfully")
    return raise_error(404, "Course not found")