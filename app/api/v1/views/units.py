from app.api.v1 import units_blueprint_v1
from flask_jwt_extended import jwt_required
from utils.authorization import admin_required
from utils.utils import check_units_keys, raise_error, check_unit_name_key, check_unit_code_key
from flask import request, make_response, jsonify
from app.api.v1.models.units import UnitsModel
import json
from utils.serializer import Serializer


@units_blueprint_v1.route('/units', methods=['POST'])
@jwt_required
@admin_required
def add_unit():
    """Add a new unit."""
    errors = check_units_keys(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    unit_name = details['unit_name']
    unit_code = details['unit_code']
    unitName = UnitsModel().get_unit_by_name(unit_name)
    if unitName:
        return raise_error(400, '{} already exists'.format(unit_name))
    unitCode = UnitsModel().get_unit_by_code(unit_code)
    if unitCode:
        return raise_error(400, '{} already exists'.format(unit_code))
    response = UnitsModel(unit_name, unit_code).save()
    return Serializer.serialize(response, 201, 'Unit added successfully')


@units_blueprint_v1.route('/units', methods=['GET'])
@jwt_required
@admin_required
def get_units():
    """Fetch all available units."""
    response = UnitsModel().get_units()
    return Serializer.serialize(response, 200, 'Units succesfully retrieved')


@units_blueprint_v1.route('/units/<int:unit_id>', methods=['GET'])
@jwt_required
@admin_required
def get_unit_by_id(unit_id):
    """Fetch a unit by id."""
    response = UnitsModel().get_unit_by_id(unit_id)
    if response:
        return Serializer.serialize(response, 200, "Unit successfully retrieved")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/unit_name/<string:unit_name>', methods=['GET'])
@jwt_required
@admin_required
def get_unit_by_name(unit_name):
    """Fetch a unit by name."""
    response = UnitsModel().get_unit_by_name(unit_name)
    if response:
        return Serializer.serialize(response, 200, "Unit successfully retrieved")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/unit_code/<string:unit_code>', methods=['GET'])
@jwt_required
@admin_required
def get_unit_by_code(unit_code):
    """Fetch a unit by code."""
    response = UnitsModel().get_unit_by_code(unit_code)
    if response:
        return Serializer.serialize(response, 200, "Unit successfully retrieved")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/<int:unit_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_unit(unit_id):
    """Delete a unit by id."""
    response = UnitsModel().get_unit_by_id(unit_id)
    if response:
        UnitsModel().delete(unit_id)
        return Serializer.serialize(response, 200, "Unit deleted successfully")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/<int:unit_id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_unit(unit_id):
    """Update a unit."""
    errors = check_units_keys(request)
    if errors:
        return Serializer.serialize(errors, 400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    unit_name = details['unit_name']
    unit_code = details['unit_code']
    unitName = UnitsModel().get_unit_by_name(unit_name)
    if unitName:
        return raise_error(400, '{} already exists'.format(unit_name))
    unitCode = UnitsModel().get_unit_by_code(unit_code)
    if unitCode:
        return raise_error(400, '{} already exists'.format(unit_code))
    response = UnitsModel().edit(unit_name, unit_code, unit_id)
    if response:
        return Serializer.serialize(response, 200, "Unit updated successfully")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/unit_name/<int:unit_id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_unit_name(unit_id):
    """Update a unit name."""
    errors = check_unit_name_key(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    unit_name = details['unit_name']
    unitName = UnitsModel().get_unit_by_name(unit_name)
    if unitName:
        return raise_error(400, '{} already exists'.format(unit_name))
    response = UnitsModel().edit_name(unit_name, unit_id)
    if response:
        return Serializer.serialize(response, 200, "Unit name updated successfully")
    return raise_error(404, "Unit not found")


@units_blueprint_v1.route('/units/unit_code/<int:unit_id>', methods=['PUT'])
@jwt_required
@admin_required
def edit_unit_code(unit_id):
    """Update a unit code."""
    errors = check_unit_code_key(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    unit_code = details['unit_code']
    unitCode = UnitsModel().get_unit_by_code(unit_code)
    if unitCode:
        return raise_error(400, '{} already exists'.format(unit_code))
    response = UnitsModel().edit_code(unit_code, unit_id)
    if response:
        return Serializer.serialize(response, 200, "Unit code updated successfully")
    return raise_error(404, "Unit not found")
