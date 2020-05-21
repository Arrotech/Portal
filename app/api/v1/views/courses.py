import json
from flask import request
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from app.api.v1 import courses_v1
from app.api.v1.models.courses import CoursesModel
from app.api.v1.models.departments import DepartmentsModel
from utils.utils import raise_error, check_courses_keys
from utils.authorization import admin_required

@courses_v1.route('/courses', methods=['POST'])
@jwt_required
def add_course():
    """Add a course."""
    errors = check_courses_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    course_name = details['course_name']
    department_id = details['department_id']
    if CoursesModel().get_course_name(course_name):
        return raise_error(400, '{} already exists'.format(course_name))
    if DepartmentsModel().get_department_by_id(department_id):
        response = CoursesModel(course_name, department_id).save()
        return Serializer.serialize(response, 201, "{} added successfully".format(course_name))
    return raise_error(404, "Department not found")

@courses_v1.route('/courses', methods=['GET'])
@jwt_required
def get_courses():
    """Fetch all courses."""
    response = CoursesModel().get_courses()
    return Serializer.serialize(response, 200, "Courses successfull retrieved")

@courses_v1.route('/courses/<int:course_id>', methods=['GET'])
@jwt_required
def get_course(course_id):
    """Fetch course by id."""
    response = CoursesModel().get_course_by_id(course_id)
    if response:
        return Serializer.serialize(response, 200, "Course successfull retrieved")
    return raise_error(404, "Course not found")

@courses_v1.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_course(course_id):
    """Update a course by id."""
    details = request.get_json()
    errors = check_courses_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    course_name = details['course_name']
    department_id = details['department_id']
    if CoursesModel().get_course_name(course_name):
        return raise_error(400, "{} already exists".format(course_name))
    response = CoursesModel().edit_course(course_name, department_id, course_id)
    if response:
        return Serializer.serialize(response, 200, 'Course updated successfully')
    return raise_error(404, "Course not found")