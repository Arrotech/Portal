import json

from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.certificates import CertificatesModel
from utils.utils import check_certificates_keys, raise_error, certificate_restrictions
from utils.serializer import Serializer
from utils.authorization import admin_required
from app.api.v1 import certificates_v1


@certificates_v1.route('/certificates', methods=['POST'])
@jwt_required
@admin_required
def add_certificate():
    """Add new certificate."""
    errors = check_certificates_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    certificate_name = details['certificate_name']
    if not certificate_restrictions(certificate_name):
        return raise_error(400, "Invalid certificate name")
    response = CertificatesModel(certificate_name).save()
    return Serializer.serialize(response, 201, "Certificate added successfully")