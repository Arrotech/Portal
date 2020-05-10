import json
from .base_test import BaseTest
from utils.dummy import new_hostel, new_account, hostel_keys, hostel_name_exists


class TestHostels(BaseTest):
    """Test hostels endpoints."""

    def test_add_hostel(self):
        """Test that an admin user can add a new hostel."""
        response1 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Hostel added successfully')
        assert response1.status_code == 201

    def test_hostel_keys(self):
        """Test that an admin user cannot add a new hostel with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/hostels', data=json.dumps(hostel_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid hostel_name key')
        assert response1.status_code == 400

    def test_hostel_name_exists(self):
        """Test that an admin user cannot add an existing hostel name."""
        response = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.post(
            '/api/v1/hostels', data=json.dumps(hostel_name_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'nyati already exists')
        assert response1.status_code == 400
        
    def test_get_all_hostels(self):
        """Test that a user can fetch all hostels."""
        response1 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/hostels', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Hostels retrived successfully')
        assert response2.status_code == 200