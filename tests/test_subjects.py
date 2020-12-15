import json

from utils.v1.dummy.subjects import new_subject, new_subject_keys, unexisting_user
from utils.v1.dummy.units import new_unit
from utils.v1.dummy.students_accounts import new_student_account
from .base_test import BaseTest


class TestSubjects(BaseTest):
    """Test subjects."""

    def test_add_subjects(self):
        """Test that a student can register for a subject."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'You have successfully registered Calculus 1')
        assert response.status_code == 201

    def test_add_subjects_keys(self):
        """Test that a student cannot register for a subject with an invalid key."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response.status_code == 400

    def test_add_subjects_for_unexisting_unit(self):
        """Test that an existing user cannot register for a non existing unit."""
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit Calculus 1 not found')
        assert response.status_code == 404

    def test_add_subjects_for_unexisting_user(self):
        """Test that an existing user cannot register for a non existing user."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(unexisting_user), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response.status_code == 404

    def test_get_subjects(self):
        """Test that an admin can fetch all subjects."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/subjects', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Subjects successfull retrieved')
        assert response.status_code == 200

    def test_get_subjects_by_admission(self):
        """Test that a student can fetch all subjects that they have registered for."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/subjects/NJCF1001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Subjects successfull retrieved')
        assert response.status_code == 200

    def test_delete_subject_by_id(self):
        """Test that an admin can delete a subject by id."""
        self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response = self.client.delete(
            '/api/v1/subjects/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Subject deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_subject_by_id(self):
        """Test that an admin cannot delete non existing subject by id."""
        self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response = self.client.delete(
            '/api/v1/subjects/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Subject not found')
        assert response.status_code == 404
