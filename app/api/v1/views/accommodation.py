from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.accommodation import AccommodationModel
from app.api.v1.models.users_model import UsersModel
from app.api.v1.models.hostels import HostelsModel
from utils.utils import check_accommdation_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import hostel_manager
from app.api.v1 import portal_v1


@portal_v1.route('/accommodation', methods=['POST'])
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
            return Serializer.serialize(response, 201,
                                        "Hostel booked successfully")
        return raise_error(404, "Hostel not found")
    return raise_error(404, "User not found")


@portal_v1.route('/accommodation', methods=['GET'])
@jwt_required
@hostel_manager
def get_all_booked_hostels():
    """Fetch all booked hostels."""
    response = AccommodationModel().get_booked_hostels()
    return Serializer.serialize(response, 200, "Hostels retrieved successfully")


@portal_v1.route('/accommodation/<int:accommodation_id>', methods=['GET'])
@jwt_required
def get_booked_hostel_by_id(accommodation_id):
    """Fetch hostel accommodation by id."""
    response = AccommodationModel().get_booked_hostel_by_id(accommodation_id)
    if response:
        return Serializer.serialize(response, 200,
                                    "Hostel retrieved successfully")
    return raise_error(404, "Hostel not found")


@portal_v1.route('/accommodation/<string:admission_no>', methods=['GET'])
@jwt_required
def get_booked_hostel_by_admission(admission_no):
    """Fetch hostel accommodation by admission."""
    res = AccommodationModel().get_booked_hostel_by_admission(admission_no)
    if res:
        return Serializer.serialize(res, 200,
                                    "Hostel retrieved successfully")
    return raise_error(404, "Hostel not found")


@portal_v1.route('/accommodation/all/<string:admission_no>', methods=['GET'])
@jwt_required
def get_accommodation_history_by_admission_no(admission_no):
    """Fetch accommodation history by admission number."""
    response = AccommodationModel().\
        get_accommodation_history_by_admission_no(admission_no)
    return Serializer.serialize(response, 200,
                                "Accomodation history retrieved successfully")


@portal_v1.route('/accommodation/<int:accommodation_id>', methods=['PUT'])
@jwt_required
def update_hostel_accomodation(accommodation_id):
    """Update specific hostel accommodation by id."""
    details = request.get_json()
    hostel_name = details['hostel_name']
    response = AccommodationModel().update(hostel_name, accommodation_id)
    if response:
        return Serializer.serialize(response, 200,
                                    'Hostel accommodation updated successfully')
    return raise_error(404, "Hostel accommodation not found")


@portal_v1.route('/accommodation/<int:accommodation_id>', methods=['DELETE'])
@jwt_required
def delete_hostel_accomodation(accommodation_id):
    """Delete specific hostel accommodation booking by id."""
    response = AccommodationModel().get_booked_hostel_by_id(accommodation_id)
    if response:
        AccommodationModel().delete(accommodation_id)
        return Serializer.serialize(response, 200,
                                    "Hostel accommodation deleted successfully")
    return raise_error(404, 'Hostel accommodation not found')
