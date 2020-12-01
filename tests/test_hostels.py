import json
from .base_test import BaseTest
from utils.v1.dummy.hostels import new_hostel, hostel_keys, hostel_name_exists


class TestHostels(BaseTest):
    """Test hostels endpoints."""

    def test_add_hostel(self):
        """Test that an admin user can add a new hostel."""
        response = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel added successfully')
        assert response.status_code == 201

    def test_hostel_keys(self):
        """Test that an admin user cannot add a new hostel with invalid json keys."""
        response = self.client.post(
            '/api/v1/hostels', data=json.dumps(hostel_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid hostel_name key')
        assert response.status_code == 400

    def test_hostel_name_exists(self):
        """Test that an admin user cannot add an existing hostel name."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/hostels', data=json.dumps(hostel_name_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'nyati already exists')
        assert response.status_code == 400

    def test_get_all_hostels(self):
        """Test that a user can fetch all hostels."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostels retrived successfully')
        assert response.status_code == 200

    def test_get_hostel_by_id(self):
        """Test that a user can fetch a hostel by id."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel retrived successfully')
        assert response.status_code == 200
        
    def test_get_hostel_by_name(self):
        """Test that a user can fetch a hostel by name."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels/nyati', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel retrived successfully')
        assert response.status_code == 200

    def test_get_non_existing_hostel_by_id(self):
        """Test that a user cannot fetch non existing hostel by id."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels/100', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel not found')
        assert response.status_code == 404
        
    def test_get_non_existing_hostel_by_name(self):
        """Test that a user cannot fetch non existing hostel by name."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels/ndovu', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel not found')
        assert response.status_code == 404

    def test_view_hostel_by_location(self):
        """Test that a user can view hostel(s) by location."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/hostels/location/sunrise', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel(s) retrived successfully')
        assert response.status_code == 200

    def test_delete_hostel(self):
        """Test that an admin user can delete a hostel by id."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/hostels/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel deleted successfully')
        assert response.status_code == 200

    def test_delete_unexisting_hostel(self):
        """Test that an admin user cannot delete unexisting hostel."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/hostels/100', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel not found')
        assert response.status_code == 404
