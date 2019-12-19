import json

from flask import request, jsonify, make_response, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.studentId_model import StudentIdModel

id_v1 = Blueprint('id_v1', __name__)


@id_v1.route('/id', methods=['POST'])
@jwt_required
def add_id():
    """Add a new Id."""
    details = request.get_json()
    surname = details['surname']
    first_name = details['first_name']
    last_name = details['last_name']
    admission_no = details['admission_no']

    studentId = StudentIdModel(surname,
                               first_name,
                               last_name,
                               admission_no).save()
    studentId = json.loads(studentId)
    return make_response(jsonify({
        "status": "201",
        "message": "Id assigned successfully",
        "studentId": studentId
    }), 201)

@id_v1.route('/id', methods=['GET'])
@jwt_required
def get_ids():
    """View id credentials."""
    return make_response(jsonify({
        "status": "200",
        "message": "Retrieved successfully",
        "students": json.loads(StudentIdModel().get_all())
    }), 200)

@id_v1.route('/id/<string:admission_no>', methods=['GET'])
@jwt_required
def get(admission_no):
    """Get id by admission number."""
    student = StudentIdModel().get_admission_no(admission_no)
    student = json.loads(student)
    if student:
        return make_response(jsonify({
            "status": "200",
            "message": "success",
            "Exam": student
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Id Not Found"
    }), 404)
