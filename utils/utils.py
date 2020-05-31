import re
import os

from flask import jsonify, make_response, url_for, current_app
from itsdangerous import URLSafeTimedSerializer


def check_register_keys(request):
    res_keys = ['firstname', 'lastname', 'surname',
                'admission_no', 'gender', 'email', 'password', 'current_year']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_update_user_keys(request):
    res_keys = ['firstname', 'lastname', 'surname']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_campuses_keys(request):
    res_keys = ['campus_name', 'campus_location']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_apply_course_keys(request):
    res_keys = ['admission_no', 'department_name', 'course_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_checklist_keys(request):
    res_keys = ['admission_no', 'department_name',
                'course_name', 'hostel_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_department_keys(request):
    res_keys = ['department_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_courses_keys(request):
    res_keys = ['course_name', 'department_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_promote_student_keys(request):
    res_keys = ['current_year']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_units_keys(request):
    res_keys = ['unit_name', 'unit_code']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_unit_name_key(request):
    res_keys = ['unit_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_unit_code_key(request):
    res_keys = ['unit_code']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_staff_keys(request):
    """Check that registration json keys match the required ones."""
    res_keys = ['firstname', 'lastname',
                'form', 'stream', 'username', 'email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_accountant_keys(request):
    """Check that registration json keys match the required ones."""
    res_keys = ['firstname', 'lastname', 'username', 'email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_login_keys(request):
    """Check that login json keys match the required ones."""
    res_keys = ['email', 'password']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_exams_keys(request):
    res_keys = ['semester', 'year', 'admission_no', 'unit_name', 'marks']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_fees_keys(request):
    res_keys = ['admission_no', 'transaction_type',
                'transaction_no', 'description', 'amount']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_edit_fees_keys(request):
    res_keys = ['transaction_type',
                'transaction_no', 'description', 'amount']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_library_keys(request):
    res_keys = ['admission_no', 'title', 'author',
                'book_no']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_edit_library_keys(request):
    res_keys = ['title', 'author',
                'book_no']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_hostels_keys(request):
    res_keys = ['hostel_name', 'rooms', 'gender', 'hostel_location']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_accommdation_keys(request):
    res_keys = ['admission_no', 'hostel_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def check_subjects_keys(request):
    res_keys = ['admission_no', 'unit_name']
    errors = []
    for key in res_keys:
        if not key in request.json:
            errors.append(key)
    return errors


def raise_error(status, msg):
    return make_response(jsonify({
        "status": "400",
        "message": msg
    }), status)


def is_valid_email(variable):
    """Check if email is a valid mail."""
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+[a-zA-Z0-9-.]+$)",
                variable):
        return True
    return False


def is_valid_password(variable):
    """Check if password is a valid password."""
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", variable):
        return True
    return False


def form_restrictions(data):
    """Restrict user inputs in a list."""

    form = ["1", "2", "3", "4"]
    if data not in form:
        return False
    return True

def campus_restrictions(data):
    """Restrict user inputs in a list."""

    campus_name = ["main", "town"]
    if data not in campus_name:
        return False
    return True


def term_restrictions(data):
    """Restrict user inputs in a list."""

    term = ["1st", "2nd", "3rd", "1ST", "2ND", "3RD"]
    if data not in term:
        return False
    return True


def type_restrictions(data):
    """Restrict user inputs in a list."""

    exam_type = ["main", "MAIN", "CAT", "cat"]
    if data not in exam_type:
        return False
    return True


def subjects(data):
    """Restrict user inputs in a list."""

    subject = ["R", "r", "NR", "nr"]
    if data not in subject:
        return False
    return True


def bad_request(e):
    """Capture bad request error."""
    return make_response(jsonify({
        "status": "400",
        "message": "bad request"
    }), 400)


def page_not_found(e):
    """Capture not found error."""
    return make_response(jsonify({
        "status": "404",
        "message": "resource not found"
    }), 404)


def method_not_allowed(e):
    """Capture method not allowed error."""
    return make_response(jsonify({
        "status": "405",
        "message": "method not allowed"
    }), 405)


def internal_server_error(e):
    """Capture internal server error."""
    return make_response(jsonify({
        "status": "500",
        "message": "internal server error"
    }), 500)


def default_encode_token(email, salt='email-confirm-key'):
    """Encode token using email."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=salt)


def default_decode_token(token, salt='email-confirm-key', expiration=3600):
    """Decode token and get the email."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt='email-confirm-key', max_age=expiration)
        return email
    except Exception as e:
        return False


def generate_url(endpoint, token):
    """Generate url to concatenate at the end of another url."""
    return url_for(endpoint, token=token, _external=True)
