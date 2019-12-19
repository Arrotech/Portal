import json

from flask import make_response, jsonify, request, Blueprint
from flask_restful import Resource

from app.api.v1.models.fees_models import FeesModels
from app.api.v1.models.users_model import UsersModel
from utils.bursar import bursar_required
from flask_jwt_extended import jwt_required

fees_v1 = Blueprint('fees_v1', __name__)


@fees_v1.route('/fees', methods=['POST'])
@jwt_required
@bursar_required
def add_fees():
    """Accountant can add a new fee entry."""
    details = request.get_json()
    admission_no = details['admission_no']
    transaction_type = details['transaction_type']
    transaction_no = details['transaction_no']
    description = details['description']
    amount = details['amount']
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        deposit = FeesModels(admission_no,
                                transaction_type,
                                transaction_no,
                                description,
                                amount).save()
        deposit = json.loads(deposit)
        return make_response(jsonify({
            "status": "201",
            "message": "Entry made successsfully",
            "deposit": deposit
        }), 201)
    return make_response(jsonify({
        "status": "404",
        "message": "Student with that Admission Number does not exitst."
    }), 404)

@fees_v1.route('/fees', methods=['GET'])
@jwt_required
@bursar_required
def get_fees():
    """The Accountant can view the fees structures."""
    return make_response(jsonify({
        "status": "200",
        "message": "successfully retrieved",
        "fees": json.loads(FeesModels().get_all_fees())
    }), 200)

@fees_v1.route('/fees/<string:admission_no>', methods=['GET'])
@jwt_required
def get_fee(admission_no):
    """The students can view a specific fee structure by Admission Number."""
    fee = FeesModels().get_admission_no(admission_no)
    fee = json.loads(fee)
    if fee:
        return make_response(jsonify({
            "status": "200",
            "message": "successfully retrieved",
            "Fee": fee
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Fees Not Found"
    }), 404)