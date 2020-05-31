import json

from utils.dummy import new_campus, campus_keys, campus_name_restrictions
from .base_test import BaseTest


class TestCampuses(BaseTest):
    """Test campus endoints."""

    def test_add_campus(self):
        """Test that an admin can add a new campus."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Campus added successfully')
        assert response1.status_code == 201
        
    def test_add_campus_keys(self):
        """Test that an admin cannot add a new campus with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Invalid campus_name key')
        assert response1.status_code == 400
        
    def test_add_campus_name_restrictions(self):
        """Test that an admin cannot add a new campus with invalid campus name."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Campus should either be main or town.')
        assert response1.status_code == 400