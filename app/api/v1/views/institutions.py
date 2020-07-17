import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.institutions import InstitutionsModel
from utils.utils import check_institutions_keys, raise_error
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import institutions_v1


@institutions_v1.route('/institutions', methods=['POST'])
@jwt_required
@admin_required
def add_institution():
    """Add new institution."""
    errors = check_institutions_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    institution_name = details['institution_name']
    response = InstitutionsModel(institution_name).save()
    return Serializer.serialize(response, 201, "Institution added successfully")