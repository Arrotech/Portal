import json
from tests.base_test import BaseTest
from utils.v1.dummy.academic_year import new_academic_year,\
    academic_year_keys, update_year, update_year_keys


class TestacademicYear(BaseTest):
    """Test academic year endpoints."""

    def test_add_academic_year(self):
        """Test add a new academic year."""
        response = self.client.post('/api/v1/year',
                                    data=json.dumps(new_academic_year),
                                    content_type='application/json',
                                    headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Year added successfully')
        assert response.status_code == 201

    def test_add_academic_year_keys(self):
        """Test that an admin cannot add new year with invalid json keys."""
        response = self.client.post('/api/v1/year',
                                    data=json.dumps(academic_year_keys),
                                    content_type='application/json',
                                    headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid year key')
        assert response.status_code == 400

    def test_get_years(self):
        """Test that an admin can fetch all academic years."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/year',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Years retrieved successfully')
        assert response.status_code == 200

    def test_get_year(self):
        """Test that an admin can fetch a specific year by id."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/year/1',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Year retrieved successfully')
        assert response.status_code == 200

    def test_get_non_existing_year(self):
        """Test that an admin cannot fetch non-existing year by id."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/year/100',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Year not found')
        assert response.status_code == 404

    def test_update_year(self):
        """Test that an admin user can update a department name."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.put('/api/v1/year/1',
                                   data=json.dumps(update_year),
                                   content_type='application/json',
                                   headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Year updated successfully')
        assert response.status_code == 200

    def test_update_year_keys(self):
        """An admin user cannot update an year with invalid json keys."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.put('/api/v1/year/1',
                                   data=json.dumps(update_year_keys),
                                   content_type='application/json',
                                   headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid year key')
        assert response.status_code == 400

    def test_update_non_existing_year(self):
        """Test that an admin user cannot update non-existing year."""
        response = self.client.put('/api/v1/year/10',
                                   data=json.dumps(update_year),
                                   content_type='application/json',
                                   headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Year not found')
        assert response.status_code == 404

    def test_delete_an_year(self):
        """Test that an admin can delete an year by id."""
        self.client.post('/api/v1/year',
                         data=json.dumps(new_academic_year),
                         content_type='application/json',
                         headers=self.get_registrar_token())
        response = self.client.delete('/api/v1/year/1',
                                      content_type='application/json',
                                      headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Year deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_year(self):
        """Test that an admin user cannot delete non existing year."""
        response = self.client.delete('/api/v1/year/10',
                                      content_type='application/json',
                                      headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Year not found')
        assert response.status_code == 404
