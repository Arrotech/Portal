import json

from flask import request
from flask_restful import Resource

from app.api.v1.models.fees_models import FeesModels
from app.api.v1.models.users_model import UsersModel
from utils.bursar import accountant_required
from utils.utils import check_fees_keys, raise_error, check_edit_fees_keys
from flask_jwt_extended import jwt_required
from app.api.v1 import portal_v1
from utils.serializer import Serializer


@portal_v1.route('/fees', methods=['POST'])
@jwt_required
@accountant_required
def add_fees():
    """Accountant can add a new fee entry."""
    errors = check_fees_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    transaction_type = details['transaction_type']
    transaction_no = details['transaction_no']
    description = details['description']
    amount = details['amount']
    if UsersModel().get_user_by_admission(admission_no):
        response = FeesModels(admission_no,
                              transaction_type,
                              transaction_no,
                              description,
                              amount).save()
        if "error" in response:
            return raise_error(404, "Student not found")
        return Serializer.serialize(response, 201, "Entry made successfully")


@portal_v1.route('/fees', methods=['GET'])
@jwt_required
@accountant_required
def get_fees():
    """The Accountant can view the all fees."""
    response = FeesModels().get_all_fees()
    return Serializer.serialize(response, 200, "Fees retrieved successfully")


@portal_v1.route('/fees/<string:admission_no>', methods=['GET'])
@jwt_required
def get_fees_for_one_student_by_admission(admission_no):
    """The students can view their fees by admission."""
    response = FeesModels().get_fee_by_user_admission(admission_no)
    if response:
        return Serializer.serialize(response, 200, "Fees retrieved successfully")
    return raise_error(404, "Student not found")


@portal_v1.route('/fees/<int:fee_id>', methods=['PUT'])
@jwt_required
@accountant_required
def put(fee_id):
    """Edit fees."""
    errors = check_edit_fees_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    transaction_type = details['transaction_type']
    transaction_no = details['transaction_no']
    description = details['description']
    amount = details['amount']
    response = FeesModels().edit_fees(
        transaction_type, transaction_no, description, amount, fee_id)
    if response:
        return Serializer.serialize(response, 200, "Fees updated successfully")
    return raise_error(404, "Fees not found")
