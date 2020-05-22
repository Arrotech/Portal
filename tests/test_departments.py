import json
from .base_test import BaseTest
from utils.dummy import new_department, department_name_exists, invalid_department_name_key,\
    update_department, updated_department_keys, update_department_name_exists


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
        self.assertEqual(result['message'],
                         'mathematics department already exists')
        assert response1.status_code == 400

    def test_get_departments(self):
        """Test that a user can fetch all departments."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/departments', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Departments successfully retrieved')
        assert response1.status_code == 200

    def test_get_department(self):
        """Test that a user can fetch a specific department by id."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/departments/1', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Department successfully retrieved')
        assert response1.status_code == 200

    def test_get_department_non_existing_department(self):
        """Test that a user cannot fetch non existing department by id."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/departments/100', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Department not found')
        assert response1.status_code == 404

    def test_update_department(self):
        """Test that an admin user can update a department name."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.put('/api/v1/departments/1', data=json.dumps(update_department),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Department updated successfully')
        assert response1.status_code == 200

    def test_update_department_keys(self):
        """Test that an admin user cannot update a department name with an invalid json key."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.put('/api/v1/departments/1', data=json.dumps(updated_department_keys),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid department_name key')
        assert response1.status_code == 400

    def test_update_department_name_exists(self):
        """Test that an admin user cannot update a department name with an existing department name."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.put('/api/v1/departments/1', data=json.dumps(update_department_name_exists),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'mathematics department already exists')
        assert response1.status_code == 400

    def test_update_non_existing_department(self):
        """Test that an admin user cannot update non existing department."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.put('/api/v1/departments/100', data=json.dumps(update_department),
                                    content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Department not found')
        assert response1.status_code == 404

    def test_delete_department(self):
        """Test that an admin user can delete a department."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.delete('/api/v1/departments/1',
                                       content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Department deleted successfully')
        assert response1.status_code == 200

    def test_delete_non_existing_department(self):
        """Test that an admin user cannot delete non existing department."""
        response = self.client.post('/api/v1/departments', data=json.dumps(new_department),
                                    content_type='application/json', headers=self.get_admin_token())
        response1 = self.client.delete('/api/v1/departments/10',
                                       content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Department not found')
        assert response1.status_code == 404
