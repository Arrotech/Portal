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


@certificates_v1.route('/certificates', methods=['GET'])
@jwt_required
def get_all_certificates():
    """Get all certificates."""
    response = CertificatesModel().get_all_certificates()
    return Serializer.serialize(response, 200, "Certificates retrieved successfully")


@certificates_v1.route('/certificates/<int:certificate_id>', methods=['GET'])
@jwt_required
@admin_required
def get_certificate_by_id(certificate_id):
    """Get certificate by id."""
    response = CertificatesModel().get_certificate_by_id(certificate_id)
    if response:
        return Serializer.serialize(response, 200, "Certificate retrieved successfully")
    return raise_error(404, "Certificate not found")


@certificates_v1.route('/certificates/<int:certificate_id>', methods=['PUT'])
@jwt_required
@admin_required
def update_certificate(certificate_id):
    """Update a certificate by id."""
    details = request.get_json()
    errors = check_certificates_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    certificate_name = details['certificate_name']
    if not certificate_restrictions(certificate_name):
        return raise_error(400, "Invalid certificate name")
    response = CertificatesModel().edit_certificate(certificate_name, certificate_id)
    if response:
        return Serializer.serialize(response, 200, 'Certificate updated successfully')
    return raise_error(404, "Certificate not found")


@certificates_v1.route('/certificates/<int:certificate_id>', methods=['DELETE'])
@jwt_required
@admin_required
def delete_certificate(certificate_id):
    """Delete certificate by id."""
    if CertificatesModel().get_certificate_by_id(certificate_id):
        response = CertificatesModel().delete(certificate_id)
        return Serializer.serialize(response, 200, "Certificate deleted successfully")
    return raise_error(404, 'Certificate not found')