import json

from utils.v1.dummy.checklist import fill_checklist, fill_checklist_keys,\
    fill_checklist_department_not_found, fill_checklist_course_not_found, fill_checklist_hostel_not_found,\
    fill_checklist_user_not_found
from utils.v1.dummy.students_accounts import new_student_account
from utils.v1.dummy.departments import new_department
from utils.v1.dummy.courses import new_course
from utils.v1.dummy.hostels import new_hostel
from utils.v1.dummy.apply_course import apply_course
from utils.v1.dummy.accommodation import book_hostel
from utils.v1.dummy.certificates import new_certificate
from utils.v1.dummy.campuses import new_campus
from .base_test import BaseTest


class TestChecklistForm(BaseTest):
    """Test filling checklist form."""

    def test_fill_checklist_form(self):
        """Test that a student can fill checklist form."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Checklist filled successfully')
        assert response.status_code == 201

    def test_fill_checklist_form_keys(self):
        """Test that a student cannot fill checklist form with invalid json keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response.status_code == 400

    def test_fill_checklist_form_for_non_existing_department(self):
        """Test that a student cannot fill checklist form for non existing department."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_department_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response.status_code == 404

    def test_fill_checklist_form_for_non_existing_course(self):
        """Test that a student cannot fill checklist form for non existing course."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_course_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response.status_code == 404

    def test_fill_checklist_form_for_non_existing_hostel(self):
        """Test that a student cannot fill checklist form for non existing hostel."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_hostel_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel not found')
        assert response.status_code == 404

    def test_fill_checklist_form_for_non_existing_user(self):
        """Test that a student cannot fill checklist form for non existing user."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_user_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'User not found')
        assert response.status_code == 404
