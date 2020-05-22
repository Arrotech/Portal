import json

from utils.dummy import new_subject, new_unit, new_account, new_subject_keys
from .base_test import BaseTest


class TestSubjects(BaseTest):
    """Test subjects."""

    def test_add_subjects(self):
        """Test that a student can register for a subject."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'You have successfully registered 1')
        assert response3.status_code == 201

    def test_add_subjects_keys(self):
        """Test that a student cannot register for a subject with an invalid key."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Invalid user_id key')
        assert response3.status_code == 400

    def test_add_subjects_for_unexisting_unit(self):
        """Test that an existing user cannot register for a non existing unit."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Unit 1 not found')
        assert response2.status_code == 404

    def test_add_register_for_existing_subject(self):
        """Test that a student cannot register for a subject twice."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'User does not exist or your are trying to enter marks twice')
        assert response4.status_code == 400

    def test_get_subjects(self):
        """Test that an admin can fetch all subjects."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/subjects', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Subjects successfull retrieved')
        assert response4.status_code == 200

    def test_get_subjects_by_id(self):
        """Test that a student can fetch all subjects that they have registered for."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/subjects/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Subjects successfull retrieved')
        assert response4.status_code == 200

    def test_delete_subject_by_id(self):
        """Test that an admin can delete a subject by id."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.delete(
            '/api/v1/subjects/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Subject deleted successfully')
        assert response4.status_code == 200

    def test_delete_non_existing_subject_by_id(self):
        """Test that an admin cannot delete non existing subject by id."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.delete(
            '/api/v1/subjects/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Subject not found')
        assert response4.status_code == 404
