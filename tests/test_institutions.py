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
