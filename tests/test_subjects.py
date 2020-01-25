import json

from utils.dummy import new_subject, new_account, edit_subjects
from .base_test import BaseTest


class TestSubjects(BaseTest):
    """Test subjects."""
    def test_add_subjects(self):
        """Test that the add subjects endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Subjects registered successfully!')
        assert response.status_code == 201

    def test_add_subjects_for_unexisting_user(self):
        """Test that the add subjects for unexisting user endpoint works."""
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student with that Admission Number does not exitst.')
        assert response.status_code == 404

    def test_get_subjects(self):
        """Test fetching all subjects that have been created."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/subjects', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         "successfully retrieved")
        assert response1.status_code == 200

    def test_get_subject(self):
        """Test getting a specific subject by admission_no."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/subjects/NJCF4001', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'success')
        assert response1.status_code == 200

    def test_get_unexisting_subject(self):
        """Test getting unexisting specific test_get_unexisting_subject by admission_no."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/subjects/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Subject Not Found')
        assert response1.status_code == 404

    def test_edit_subjects(self):
        """Test edit subjects."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.put(
            '/api/v1/subjects/1', data=json.dumps(edit_subjects), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'subjects updated successfully')
        assert response2.status_code == 200

    def test_edit_unexisting_subjects(self):
        """Test edit unexisting subjects."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/subjects', data=json.dumps(new_subject), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.put(
            '/api/v1/subjects/1000', data=json.dumps(edit_subjects), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'subjects not found')
        assert response2.status_code == 404
