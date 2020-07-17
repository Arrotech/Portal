import json

from utils.dummy import new_institution, institution_keys
from .base_test import BaseTest


class TestInstitutions(BaseTest):
    """Test institutions endpoints."""

    def test_add_institution(self):
        """Test that an admin can add a new institution."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Institution added successfully')
        assert response1.status_code == 201

    def test_add_institution_keys(self):
        """Test that an admin cannot add a new institution with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(institution_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Invalid institution_name key')
        assert response1.status_code == 400

    def test_get_all_institutions(self):
        """Test that a user can fetch all institutions."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/institutions', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Institutions retrieved successfully')
        assert response2.status_code == 200

    def test_get_institution_by_id(self):
        """Test that an admin can fetch institution by id."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/institutions/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Institution retrieved successfully')
        assert response2.status_code == 200

    def test_get_non_existing_institution_by_id(self):
        """Test that an admin cannot fetch non existing institution by id."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/institutions/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response2.status_code == 404

    def test_delete_institution(self):
        """Test that an admin can delete existing institution."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/institutions/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Institution deleted successfully')
        assert response2.status_code == 200
        
    def test_delete_non_existing_institution(self):
        """Test that an admin cannot delete non existing institution."""
        response1 = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.delete(
            '/api/v1/institutions/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response2.status_code == 404