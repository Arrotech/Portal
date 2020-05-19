import json
from .base_test import BaseTest
from utils.dummy import new_department, department_name_exists, invalid_department_name_key

class TestDepartments(BaseTest):
    """Test departments endpoints."""
    def test_add_department(self):
        """Test add a new department."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Department added successfully')
        assert response.status_code == 201
        
    def test_add_department_json_keys(self):
        """Test add a new department json keys."""
        response = self.client.post('/api/v1/departments', data=json.dumps(invalid_department_name_key),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid department_name key')
        assert response.status_code == 400
        
    def test_department_name_exists(self):
        """Test that an admin cannot add an existing department name."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.post('/api/v1/departments', data=json.dumps(department_name_exists),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'mathematics department already exists')
        assert response1.status_code == 400

