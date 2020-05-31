import json

from utils.dummy import new_campus, campus_keys, campus_name_restrictions, update_campus,\
    update_campus_keys, update_campus_name_restrictions
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
        
    def test_update_campus(self):
        """Test that an admin can update an existing campus."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus updated successfully')
        assert response2.status_code == 200

    def test_update_campus_keys(self):
        """Test that an admin cannot update existing campus with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Invalid campus_name key')
        assert response2.status_code == 400

    def test_update_campus_name_restrictions(self):
        """Test that an admin cannot update a campus with invalid campus name."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/campuses/1', data=json.dumps(update_campus_name_restrictions), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus should either be main or town.')
        assert response2.status_code == 400
        
    def test_update_non_existing_campus(self):
        """Test that an admin cannot update non existing campus."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/campuses/100', data=json.dumps(update_campus), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response2.status_code == 404
        
    def test_delete_campus(self):
        """Test that an admin can delete existing campus."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/campuses/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus deleted successfully')
        assert response2.status_code == 200
        
    def test_delete_non_existing_campus(self):
        """Test that an admin cannot delete non existing campus."""
        response1 = self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/campuses/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response2.status_code == 404
