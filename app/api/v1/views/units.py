from app.api.v1 import units_blueprint_v1
from flask_jwt_extended import jwt_required
from utils.authorization import admin_required
from utils.utils import check_units_keys, raise_error
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
        return Serializer.serialize(errors, 400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    unit_name = details['unit_name']
    unit_code = details['unit_code']
    unitName = UnitsModel().get_unit_by_name(unit_name)
    if unitName:
        return Serializer.serialize(unitName, 400, '{} already exists'.format(unit_name))
    unitCode = UnitsModel().get_unit_by_code(unit_code)
    if unitCode:
        return Serializer.serialize(unitCode, 400, '{} already exists'.format(unit_code))
    response = UnitsModel(unit_name, unit_code).save()
    return Serializer.serialize(response, 201, 'Unit added successfully')

@units_blueprint_v1.route('/units', methods=['GET'])
@jwt_required
@admin_required
def get_units():
    """Fetch all available units."""
    response = UnitsModel().get_units()
    return Serializer.serialize(response, 200, 'Units succesfully retrieved')


