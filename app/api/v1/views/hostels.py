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