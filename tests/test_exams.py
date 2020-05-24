import json

from utils.dummy import new_entry, new_unit, new_account, invalid_exam_key, invalid_unit_id, invalid_user_id
from .base_test import BaseTest


class TestExams(BaseTest):
    """Test Exams."""

    def test_add_exams(self):
        """Test that an admin can make a new exam entry."""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'Marks added successfully')
        assert response3.status_code == 201

    def test_add_exams_keys(self):
        """Test that an admin cannot make a new exam entry with an invalid json key."""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_exam_key), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response3.status_code == 400

    def test_add_exams_for_non_existing_unit(self):
        """Test that an admin cannot make a new exam entry for a non existing unit"""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_unit_id), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'Unit Calculus 111 not found')
        assert response3.status_code == 404

    def test_add_exams_for_non_existing_user(self):
        """Test that an admin cannot make a new exam entry for a non existing user"""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_user_id), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'User does not exist or your are trying to enter marks twice')
        assert response3.status_code == 400

    def test_get_exams(self):
        """Test that an admin can fetch all exams."""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/exams', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response4.status_code == 200

    def test_get_exams_for_a_student_by_admission(self):
        """Test that a student can fetch all exams."""
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/exams/NJCF1001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response4.status_code == 200
