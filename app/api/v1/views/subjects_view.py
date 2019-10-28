import json

from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.subject_model import SubjectsModel

subjects_v1 = Blueprint('subjects_v1', __name__)


@subjects_v1.route('/subjects', methods=['POST'])
@jwt_required
def register_subjects():
    """Create a new exam entry."""
    details = request.get_json()
    admission_no = details['admission_no']
    maths = details['maths']
    english = details['english']
    kiswahili = details['kiswahili']
    chemistry = details['chemistry']
    biology = details['biology']
    physics = details['physics']
    history = details['history']
    geography = details['geography']
    cre = details['cre']
    agriculture = details['agriculture']
    business = details['business']

    res = SubjectsModel(admission_no,
                        maths,
                        english,
                        kiswahili,
                        chemistry,
                        biology,
                        physics,
                        history,
                        geography,
                        cre,
                        agriculture,
                        business).save()
    return make_response(jsonify({
        "status": "201",
        "message": "Subjects registered successfully!",
        "subjects": res
    }), 201)

@subjects_v1.route('/subjects', methods=['GET'])
@jwt_required
def get_subjects():
    """Fetch all registered subjects."""
    return make_response(jsonify({
        "status": "200",
        "message": "successfully retrieved",
        "subjects": json.loads(SubjectsModel().get_subjects())
    }), 200)

@subjects_v1.route('/subjects/<string:admission_no>', methods=['GET'])
@jwt_required
def get_subject(admission_no):
    """Fetch one subject."""
    subject = SubjectsModel().get_admission_no(admission_no)
    subject = json.loads(subject)
    if subject:
        return make_response(jsonify({
            "status": "200",
            "message": "success",
            "subject": subject
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Subject Not Found"
    }), 404)
