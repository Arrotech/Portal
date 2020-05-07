import json
from .base_test import BaseTest
from utils.dummy import new_unit, new_account, new_unit_code, unit_keys

class TestUnits(BaseTest):
    """Test units endpoints."""
    
    def test_add_unit(self):
        """Test that an admin user can add a new unit."""
        response1 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Unit added successfully')
        assert response1.status_code == 201
        
    def test_unit_keys(self):
        """Test that an admin user cannot add a new unit with wrong keys."""
        response1 = self.client.post(
            '/api/v1/units', data=json.dumps(unit_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid unit_name key')
        assert response1.status_code == 400
        
    def test_unit_name_exists(self):
        """Test that an admin user cannot add an existing unit name."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Calculus 1 already exists')
        assert response1.status_code == 400
        
    def test_unit_code_exists(self):
        """Test that an admin user cannot add an existing unit code."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit_code), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'SMA001 already exists')
        assert response1.status_code == 400
        
    def test_get_units(self):
        """Test that an admin user can fetch all units."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/units', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Units succesfully retrieved')
        assert response1.status_code == 200
        
    def test_get_unit_by_code(self):
        """Test that an admin user can fetch a unit by code."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/units/SMA001', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Unit successfully retrieved')
        assert response1.status_code == 200
        
    def test_get_unexisting_unit_by_code(self):
        """Test that an admin user cannot fetch unexisting unit by code."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/units/SMA005', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response1.status_code == 404
    