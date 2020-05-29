import json

from utils.dummy import new_department, new_course, new_hostel, fill_checklist, fill_checklist_keys,\
    fill_checklist_department_not_found, fill_checklist_course_not_found, fill_checklist_hostel_not_found
from .base_test import BaseTest


class TestChecklistForm(BaseTest):
    """Test filling checklist form."""

    def test_fill_checklist_form(self):
        """Test that a student can fill checklist form."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Checklist filled successfully')
        assert response5.status_code == 201

    def test_fill_checklist_form_keys(self):
        """Test that a student cannot fill checklist form with invalid json keys."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response5.status_code == 400

    def test_fill_checklist_form_for_non_existing_department(self):
        """Test that a student cannot fill checklist form for non existing department."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_department_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response5.status_code == 404

    def test_fill_checklist_form_for_non_existing_course(self):
        """Test that a student cannot fill checklist form for non existing course."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_course_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response5.status_code == 404

    def test_fill_checklist_form_for_non_existing_hostel(self):
        """Test that a student cannot fill checklist form for non existing hostel."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/checklist', data=json.dumps(fill_checklist_hostel_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Hostel not found')
        assert response5.status_code == 404
