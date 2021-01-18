from app.api.v1 import portal_v1
from flask_jwt_extended import jwt_required
from utils.authorization import hostel_manager
from utils.utils import check_hostels_keys, raise_error
from flask import request
from app.api.v1.models.hostels import HostelsModel
from utils.serializer import Serializer


@portal_v1.route('/hostels', methods=['POST'])
@jwt_required
@hostel_manager
def add_hostel():
    """Add a new hostel."""
    errors = check_hostels_keys(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    hostel_name = details['hostel_name']
    rooms = details['rooms']
    gender = details['gender']
    hostel_location = details['hostel_location']
    hostelName = HostelsModel().get_hostel_by_name(hostel_name)
    if hostelName:
        return raise_error(400, '{} already exists'.format(hostel_name))
    response = HostelsModel(hostel_name, rooms, gender, hostel_location).save()
    return Serializer.serialize(response, 201, 'Hostel added successfully')


@portal_v1.route('/hostels', methods=['GET'])
@jwt_required
def get_all_hostels():
    """Have a user able to view all hostels."""
    response = HostelsModel().get_all_hostels()
    return Serializer.serialize(response, 200, "Hostels retrived successfully")


@portal_v1.route('/hostels/<int:hostel_id>', methods=['GET'])
@jwt_required
def get_hostel_by_id(hostel_id):
    """Have a user able to view hostel by id."""
    response = HostelsModel().get_hostel_by_id(hostel_id)
    if response:
        return Serializer.serialize(response, 200,
                                    "Hostel retrived successfully")
    return raise_error(404, 'Hostel not found')


@portal_v1.route('/hostels/<string:hostel_name>', methods=['GET'])
@jwt_required
def get_hostel_by_name(hostel_name):
    """Have a user able to view hostel by name."""
    response = HostelsModel().get_hostel_by_name(hostel_name)
    if response:
        return Serializer.serialize(response, 200,
                                    "Hostel retrived successfully")
    return raise_error(404, 'Hostel not found')


@portal_v1.route('/hostels/location/<string:hostel_location>', methods=['GET'])
@jwt_required
def get_hostels_by_location(hostel_location):
    """Have a user able to view all hostels by location."""
    response = HostelsModel().view_hostel_by_location(hostel_location)
    return Serializer.serialize(response, 200,
                                "Hostel(s) retrived successfully")


@portal_v1.route('/hostels/<int:hostel_id>', methods=['PUT'])
@jwt_required
@hostel_manager
def update_hostel_by_id(hostel_id):
    """Update hostel by id."""
    errors = check_hostels_keys(request)
    if errors:
        return raise_error(400, 'Invalid {} key'.format(', '.join(errors)))
    details = request.get_json()
    hostel_name = details['hostel_name']
    rooms = details['rooms']
    gender = details['gender']
    hostel_location = details['hostel_location']
    response = HostelsModel().edit_hostel(hostel_name,
                                          rooms,
                                          gender,
                                          hostel_location,
                                          hostel_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Hostel updated successfully')
    return raise_error(404, "Hostel not found")


@portal_v1.route('/hostels/<int:hostel_id>', methods=['DELETE'])
@jwt_required
@hostel_manager
def delete_hostel(hostel_id):
    """Delete a hostel by id."""
    response = HostelsModel().get_hostel_by_id(hostel_id)
    if response:
        HostelsModel().delete(hostel_id)
        return Serializer.serialize(response, 200,
                                    "Hostel deleted successfully")
    return raise_error(404, "Hostel not found")
