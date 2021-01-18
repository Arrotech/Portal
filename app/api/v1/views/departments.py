from flask import request
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from app.api.v1 import portal_v1
from app.api.v1.models.departments import DepartmentsModel
from utils.utils import raise_error, check_department_keys
from utils.authorization import college_head


@portal_v1.route('/departments', methods=['POST'])
@jwt_required
@college_head
def add_department():
    """Add a new department."""
    details = request.get_json()
    errors = check_department_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    department_name = details['department_name']
    if DepartmentsModel().get_department_name(department_name):
        return raise_error(400,
                           "{} department already exists".format(department_name))
    response = DepartmentsModel(department_name).save()
    return Serializer.serialize(response, 201, "Department added successfully")


@portal_v1.route('/departments', methods=['GET'])
@jwt_required
def get_all_departments():
    """Get all departments."""
    response = DepartmentsModel().get_all_departments()
    return Serializer.serialize(response,
                                200, 'Departments successfully retrieved')


@portal_v1.route('/departments/<int:department_id>', methods=['GET'])
@jwt_required
def get_department_by_id(department_id):
    """Get all departments."""
    response = DepartmentsModel().get_department_by_id(department_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Department successfully retrieved')
    return raise_error(404, "Department not found")


@portal_v1.route('/departments/<int:department_id>', methods=['PUT'])
@jwt_required
@college_head
def update_department(department_id):
    """Update a department by id."""
    details = request.get_json()
    errors = check_department_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    department_name = details['department_name']
    if DepartmentsModel().get_department_name(department_name):
        return raise_error(
            400,
            "{} department already exists".format(department_name))
    response = DepartmentsModel().edit_department(department_name,
                                                  department_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Department updated successfully')
    return raise_error(404, "Department not found")


@portal_v1.route('/departments/<int:department_id>', methods=['DELETE'])
@jwt_required
@college_head
def delete_department(department_id):
    """Delete department by id."""
    response = DepartmentsModel().get_department_by_id(department_id)
    if response:
        DepartmentsModel().delete(department_id)
        return Serializer.serialize(response, 200,
                                    "Department deleted successfully")
    return raise_error(404, 'Department not found')
