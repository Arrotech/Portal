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

    def test_get_all_campuses(self):
        """Test that a user can fetch all campuses."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/campuses', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campuses retrieved successfully')
        assert response2.status_code == 200

    def test_get_campus_by_id(self):
        """Test that an admin can fetch campus by id."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/campuses/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus retrieved successfully')
        assert response2.status_code == 200

    def test_get_non_existing_campus_by_id(self):
        """Test that an admin cannot fetch non existing campus by id."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/campuses/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response2.status_code == 404
