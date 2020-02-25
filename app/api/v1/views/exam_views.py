"""Json package."""
import json
import datetime

from flask import make_response, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.api.v1.models.exams_model import ExamsModel
from app.api.v1.models.users_model import UsersModel
from utils.authorization import admin_required
from utils.utils import check_exams_keys, form_restrictions, term_restrictions, type_restrictions, raise_error

exams_v1 = Blueprint('exams_v1', __name__)


@exams_v1.route('/exams', methods=['POST'])
@jwt_required
@admin_required
def add_exam():
    """Create a new exam entry for an existing user."""
    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    term = details['term']
    form = details['form']
    stream = details['stream']
    exam_type = details['exam_type']
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
    if ((details['maths'] < 0) or (details['english'] < 0) or (details['kiswahili'] < 0) or (details['chemistry'] < 0) or (details['biology'] < 0) or (details['physics'] < 0) or (details['history'] < 0) or (details['geography'] < 0) or (details['cre'] < 0) or (details['agriculture'] < 0) or (details['business'] < 0)):
        return raise_error(400, "Please add a number greater than 0")
    if ((details['maths'] > 100) or (details['english'] > 100) or (details['kiswahili'] > 100) or (details['chemistry'] > 100) or (details['biology'] > 100) or (details['physics'] > 100) or (details['history'] > 100) or (details['geography'] > 100) or (details['cre'] > 100) or (details['agriculture'] > 100) or (details['business'] > 100)):
        return raise_error(400, "Please add a number less than 100")
    user = json.loads(UsersModel().get_admission_no(admission_no))
    if user:
        exam = ExamsModel(admission_no,
                        term,
                        form,
                        stream,
                        exam_type,
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
        exam = json.loads(exam)
        return make_response(jsonify({
            "status": "201",
            "message": "Entry created successfully!",
            "exams": exam
        }), 201)
    return make_response(jsonify({
        "status": "404",
        "message": "Student with that Admission Number does not exitst."
    }), 404)


@exams_v1.route('/exams', methods=['GET'])
@jwt_required
def get_exams():
    """Get all exams entries for all students."""
    return make_response(jsonify({
        "status": "200",
        "message": "successfully retrieved",
        "exams": json.loads(ExamsModel().get_all_exams())
    }), 200)

@exams_v1.route('/exams/<string:form>/<string:term>', methods=['GET'])
@jwt_required
def get_exams_form(form, term):
    """Get all exams entries for all students by form."""
    exam = ExamsModel().get_exams_by_form_and_term(form, term)
    exam = json.loads(exam)
    if exam:
        return make_response(jsonify({
            "status": "200",
            "message": "successfully retrieved",
            "Exam": exam
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Exam Not Found"
    }), 404)

@exams_v1.route('/exams/<string:admission_no>', methods=['GET'])
@jwt_required
def get_exam(admission_no):
    """Fetch an exam by specific Admission Number."""
    exam = ExamsModel().get_exams_by_admission_no(admission_no)
    exam = json.loads(exam)
    if exam:
        return make_response(jsonify({
            "status": "200",
            "message": "successfully retrieved",
            "Exam": exam
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Exam Not Found"
    }), 404)


@exams_v1.route('/exams/<string:admission_no>', methods=['DELETE'])
@jwt_required
@admin_required
def delete(admission_no):
    """Delete an exam by Admission Number."""
    exam = ExamsModel().get_exam_by_admission_no(admission_no)
    exam = json.loads(exam)
    if exam:
        ExamsModel().delete_exam(admission_no)
        return make_response(jsonify({
            "status": "200",
            "message": "Exam deleted successfully"
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "Exam not found"
    }), 404)


@exams_v1.route('/exams/<int:exam_id>', methods=['PUT'])
@jwt_required
@admin_required
def put(exam_id):
    """Edit exams."""

    errors = check_exams_keys(request)
    if errors:
        return raise_error(400, "Invalid {} key".format(', '.join(errors)))
    details = request.get_json()
    admission_no = details['admission_no']
    term = details['term']
    form = details['form']
    stream = details['stream']
    exam_type = details['exam_type']
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

    exam = ExamsModel().edit_exams(admission_no,
                                term,
                                form,
                                stream,
                                exam_type,
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
                                business,
                                exam_id)
    exam = json.loads(exam)
    print('@@@@@@@@@@@@@@@@@@@@@@ EXAM @@@@@@@@@@@@@@@@@@@')
    print(exam)
    if exam:
        return make_response(jsonify({
            "status": "200",
            "message": "exam updated successfully",
            "new_party": exam
        }), 200)
    return make_response(jsonify({
        "status": "404",
        "message": "exam not found"
    }), 404)
