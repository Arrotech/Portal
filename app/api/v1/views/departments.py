from flask import request
from flask_jwt_extended import jwt_required
from utils.serializer import Serializer
from app.api.v1 import departments_v1
from app.api.v1.models.departments import DepartmentsModel
from utils.utils import raise_error, check_department_keys
from utils.authorization import admin_required


@departments_v1.route('/departments', methods=['POST'])
@jwt_required
@admin_required
def add_department():
    """Add a new department."""
    details = request.get_json()
    errors = check_department_keys(request)
    if errors:
        return Serializer.serialize(errors, 400, "Invalid {} key".format(', '.join(errors)))
    department_name = details['department_name']
    if DepartmentsModel().get_department_name(department_name):
        return raise_error(400, "{} department already exists".format(department_name))
    response = DepartmentsModel(department_name).save()
    return Serializer.serialize(response, 201, "Department added successfully")


@departments_v1.route('/departments', methods=['GET'])
@jwt_required
def get_all_departments():
    """Get all departments."""
    response = DepartmentsModel().get_all_departments()
    return Serializer.serialize(response, 200, 'Departments successfully retrieved')
