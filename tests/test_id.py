import json

from utils.dummy import add_student_info
from .base_test import BaseTest


class TestId(BaseTest):
    """Test Id."""
    def test_add_id(self):
        """Test that the add Id endpoint works."""
        response = self.client.post(
            '/api/v1/id', data=json.dumps(add_student_info), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Id assigned successfully')
        assert response.status_code == 201

    def test_get_ids(self):
        """Test fetching all Ids that have been created."""
        response = self.client.post(
            '/api/v1/id', data=json.dumps(add_student_info), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/id', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         "Retrieved successfully")
        assert response1.status_code == 200

    def test_get_id(self):
        """Test getting a specific id by admission_no."""

        response = self.client.post(
            '/api/v1/id', data=json.dumps(add_student_info), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/id/NJCF4001', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'success')
        assert response1.status_code == 200

    def test_get_unexisting_id(self):
        """Test getting unexisting specific id by admission_no."""

        response1 = self.client.get(
            '/api/v1/id/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Id Not Found')
        assert response1.status_code == 404
