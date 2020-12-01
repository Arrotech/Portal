import json

from utils.v1.dummy.campuses import new_campus, campus_keys, campus_name_restrictions, update_campus,\
    update_campus_keys, update_campus_name_restrictions
from .base_test import BaseTest


class TestCampuses(BaseTest):
    """Test campus endpoints."""

    def test_add_campus(self):
        """Test that an admin can add a new campus."""
        response = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus added successfully')
        assert response.status_code == 201

    def test_add_campus_keys(self):
        """Test that an admin cannot add a new campus with invalid json keys."""
        response = self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid campus_name key')
        assert response.status_code == 400

    def test_add_campus_name_restrictions(self):
        """Test that an admin cannot add a new campus with invalid campus name."""
        response = self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus should either be main or town.')
        assert response.status_code == 400

    def test_get_all_campuses(self):
        """Test that a user can fetch all campuses."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/campuses', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campuses retrieved successfully')
        assert response.status_code == 200

    def test_get_campus_by_id(self):
        """Test that an admin can fetch campus by id."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/campuses/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus retrieved successfully')
        assert response.status_code == 200

    def test_get_non_existing_campus_by_id(self):
        """Test that an admin cannot fetch non existing campus by id."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/campuses/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response.status_code == 404
        
    def test_update_campus(self):
        """Test that an admin can update an existing campus."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus updated successfully')
        assert response.status_code == 200

    def test_update_campus_keys(self):
        """Test that an admin cannot update existing campus with invalid json keys."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid campus_name key')
        assert response.status_code == 400

    def test_update_campus_name_restrictions(self):
        """Test that an admin cannot update a campus with invalid campus name."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus should either be main or town.')
        assert response.status_code == 400
        
    def test_update_non_existing_campus(self):
        """Test that an admin cannot update non existing campus."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/campuses/100', data=json.dumps(update_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response.status_code == 404
        
    def test_delete_campus(self):
        """Test that an admin can delete existing campus."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/campuses/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus deleted successfully')
        assert response.status_code == 200
        
    def test_delete_non_existing_campus(self):
        """Test that an admin cannot delete non existing campus."""
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/campuses/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response.status_code == 404
