import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.accommodation import AccommodationModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.hostels import HostelsModel
from utils.utils import check_accommdation_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import accommodation_v1


@accommodation_v1.route('/accommodation', methods=['POST'])
@jwt_required
def book_hostel():
    """Book hostel."""
    errors = check_accommdation_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    hostel_name = details['hostel_name']
    if UsersModel().get_user_by_admission(admission_no):
        if HostelsModel().get_hostel_by_name(hostel_name):
            response = AccommodationModel(admission_no, hostel_name).save()
            if "error" in response:
                return raise_error(404, "User does not exist or your are trying to book twice")
            return Serializer.serialize(response, 201, "Hostel booked successfully")
        return raise_error(404, "Hostel not found")


@accommodation_v1.route('/accommodation', methods=['GET'])
@jwt_required
@admin_required
def get_all_booked_hostels():
    """Fetch all hostels that have been booked."""
    response = AccommodationModel().get_booked_hostels()
    return Serializer.serialize(response, 200, "Hostels retrieved successfully")


@accommodation_v1.route('/accommodation/<string:admission_no>', methods=['GET'])
@jwt_required
def get_booked_hostel_by_admission(admission_no):
    """Fetch hostel by admission."""
    response = AccommodationModel().get_booked_hostel_by_admission(admission_no)
    if response:
        return Serializer.serialize(response, 200, "Hostel retrieved successfully")
    return raise_error(404, "Hostel not found")
