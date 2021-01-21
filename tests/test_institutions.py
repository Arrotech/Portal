import json

from utils.v1.dummy.institutions import new_institution, institution_keys,\
    update_institution, update_institution_keys
from tests.base_test import BaseTest


class TestInstitutions(BaseTest):
    """Test institutions endpoints."""

    def test_add_institution(self):
        """Test that an admin can add a new institution."""
        response = self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution added successfully')
        assert response.status_code == 201

    def test_add_institution_keys(self):
        """An admin cannot add a new institution with invalid json keys."""
        response = self.client.post(
            '/api/v1/institutions', data=json.dumps(institution_keys),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid institution_name key')
        assert response.status_code == 400

    def test_get_all_institutions(self):
        """Test that a user can fetch all institutions."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/institutions', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institutions retrieved successfully')
        assert response.status_code == 200

    def test_get_institution_by_id(self):
        """Test that an admin can fetch institution by id."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/institutions/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution retrieved successfully')
        assert response.status_code == 200

    def test_get_non_existing_institution_by_id(self):
        """Test that an admin cannot fetch non existing institution by id."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/institutions/10', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response.status_code == 404

    def test_update_institution(self):
        """Test that an admin can update an existing institution."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/institutions/1', data=json.dumps(update_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution updated successfully')
        assert response.status_code == 200

    def test_update_institution_keys(self):
        """An admin cannot update institution with invalid json keys."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/institutions/1', data=json.dumps(update_institution_keys),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid institution_name key')
        assert response.status_code == 400

    def test_update_non_existing_institution(self):
        """Test that an admin cannot update non existing institution."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/institutions/100', data=json.dumps(update_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response.status_code == 404

    def test_delete_institution(self):
        """Test that an admin can delete existing institution."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.delete(
            '/api/v1/institutions/1', content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_institution(self):
        """Test that an admin cannot delete non existing institution."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.delete(
            '/api/v1/institutions/100', content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response.status_code == 404
