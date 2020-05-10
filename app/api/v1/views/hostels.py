from app.api.v1 import hostels_v1
from flask_jwt_extended import jwt_required
from utils.authorization import admin_required
from utils.utils import check_hostels_keys, raise_error
from flask import request, make_response, jsonify
from app.api.v1.models.hostels import HostelsModel
import json
from utils.serializer import Serializer


@hostels_v1.route('/hostels', methods=['POST'])
@jwt_required
@admin_required
def add_hostel():
    """Add a new hostel."""
    errors = check_hostels_keys(request)
    if errors:
        return Serializer.serialize(errors, 400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    hostel_name = details['hostel_name']
    rooms = details['rooms']
    hostel_location = details['hostel_location']
    hostelName = HostelsModel().get_hostel_by_name(hostel_name)
    if hostelName:
        return raise_error(400, '{} already exists'.format(hostel_name))
    response = HostelsModel(hostel_name, rooms, hostel_location).save()
    return Serializer.serialize(response, 201, 'Hostel added successfully')


@hostels_v1.route('/hostels', methods=['GET'])
@jwt_required
def get_all_hostels():
    """Have a user able to view all hostels."""
    response = HostelsModel().get_all_hostels()
    return Serializer.serialize(response, 200, "Hostels retrived successfully")


@hostels_v1.route('/hostels/<int:hostel_id>', methods=['GET'])
@jwt_required
def get_hostel_by_id(hostel_id):
    """Have a user able to view hostel by id."""
    response = HostelsModel().get_hostel_by_id(hostel_id)
    if response:
        return Serializer.serialize(response, 200, "Hostel retrived successfully")
    return raise_error(404, 'Hostel not found')


@hostels_v1.route('/hostels/<string:hostel_location>', methods=['GET'])
@jwt_required
def get_hostels_by_location(hostel_location):
    """Have a user able to view all hostels by location."""
    response = HostelsModel().view_hostel_by_location(hostel_location)
    return Serializer.serialize(response, 200, "Hostel(s) retrived successfully")
