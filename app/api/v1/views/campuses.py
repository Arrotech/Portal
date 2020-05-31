import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.campuses import CampusModel
from utils.utils import check_campuses_keys, raise_error, campus_restrictions
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import campuses_v1


@campuses_v1.route('/campuses', methods=['POST'])
@jwt_required
@admin_required
def add_campus():
    """Add new campus."""
    errors = check_campuses_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    campus_name = details['campus_name']
    campus_location = details['campus_location']
    if not campus_restrictions(campus_name):
        return raise_error(400, "Campus should either be main or town.")
    response = CampusModel(campus_name, campus_location).save()
    return Serializer.serialize(response, 201, "Campus added successfully")


@campuses_v1.route('/campuses', methods=['GET'])
@jwt_required
def get_all_campuses():
    """Fetch all campuses."""
    response = CampusModel().get_all_campuses()
    return Serializer.serialize(response, 200, "Campuses retrieved successfully")


@campuses_v1.route('/campuses/<int:campus_id>', methods=['GET'])
@jwt_required
@admin_required
def get_campus_by_id(campus_id):
    """Fetch campus by id."""
    response = CampusModel().get_campus_by_id(campus_id)
    if response:
        return Serializer.serialize(response, 200, "Campus retrieved successfully")
    return raise_error(404, "Campus not found")


@campuses_v1.route('/campuses/<int:campus_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_campus(campus_id):
    """Update a campus by id."""
    details = request.get_json()
    errors = check_campuses_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    campus_name = details['campus_name']
    campus_location = details['campus_location']
    if not campus_restrictions(campus_name):
        return raise_error(400, "Campus should either be main or town.")
    response = CampusModel().edit_campus(campus_name, campus_location, campus_id)
    if response:
        return Serializer.serialize(response, 200, 'Campus updated successfully')
    return raise_error(404, "Campus not found")
