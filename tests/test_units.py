import json
from .base_test import BaseTest
from utils.v1.dummy.units import new_unit, new_unit_code, unit_keys, update_unit, update_existing_unit_name, update_existing_unit_code, update_unit_name, update_existing_unit_name1, update_unit_code, update_existing_unit_code1, edit_unit_keys, edit_unit_name_key, edit_unit_code_key


class TestUnits(BaseTest):
    """Test units endpoints."""

    def test_add_unit(self):
        """Test that an admin user can add a new unit."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit added successfully')
        assert response.status_code == 201

    def test_unit_keys(self):
        """Test that an admin user cannot add a new unit with wrong keys."""
        response = self.client.post(
            '/api/v1/units', data=json.dumps(unit_keys), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid unit_name key')
        assert response.status_code == 400

    def test_unit_name_exists(self):
        """Test that an admin user cannot add an existing unit name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Calculus 1 already exists')
        assert response.status_code == 400

    def test_unit_code_exists(self):
        """Test that an admin user cannot add an existing unit code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/units', data=json.dumps(new_unit_code), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'SMA001 already exists')
        assert response.status_code == 400

    def test_get_units(self):
        """Test that an admin user can fetch all units."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Units succesfully retrieved')
        assert response.status_code == 200

    def test_get_unit_by_id(self):
        """Test that an admin user can fetch a unit by id."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit successfully retrieved')
        assert response.status_code == 200

    def test_get_unexisting_unit_by_id(self):
        """Test that an admin user cannot fetch unexisting unit by id."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/50', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_get_unit_by_name(self):
        """Test that an admin user can fetch a unit by name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/unit_name/Calculus 1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit successfully retrieved')
        assert response.status_code == 200

    def test_get_unexisting_unit_by_name(self):
        """Test that an admin user cannot fetch unexisting unit by name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/unit_name/Calculus 5', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_get_unit_by_code(self):
        """Test that an admin user can fetch a unit by code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/unit_code/SMA001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit successfully retrieved')
        assert response.status_code == 200

    def test_get_unexisting_unit_by_code(self):
        """Test that an admin user cannot fetch unexisting unit by code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.get(
            '/api/v1/units/unit_code/SMA005', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_delete_unit(self):
        """Test that an admin user can delete a unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.delete(
            '/api/v1/units/1', content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit deleted successfully')
        assert response.status_code == 200

    def test_delete_unexisting_unit(self):
        """Test that an admin user cannot delete unexisting unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.delete(
            '/api/v1/units/100', content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_edit_unit(self):
        """Test that an admin user can edit a unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/1', data=json.dumps(update_unit), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit updated successfully')
        assert response.status_code == 200

    def test_edit_unit_keys(self):
        """Test that an admin user cannot edit a unit with an invalid key."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/1', data=json.dumps(edit_unit_keys), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid unit_name key')
        assert response.status_code == 400

    def test_edit_unexisting_unit(self):
        """Test that an admin user cannot edit non existing unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/100', data=json.dumps(update_unit), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_edit_existing_unit_name(self):
        """Test that an admin user cannot edit existing unit name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/1', data=json.dumps(update_existing_unit_name), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Calculus 1 already exists')
        assert response.status_code == 400

    def test_edit_existing_unit_code(self):
        """Test that an admin user cannot edit existing unit code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/1', data=json.dumps(update_existing_unit_code), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'SMA001 already exists')
        assert response.status_code == 400

    def test_edit_unit_name(self):
        """Test that an admin user can edit a unit name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_name/1', data=json.dumps(update_unit_name), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit name updated successfully')
        assert response.status_code == 200

    def test_edit_unit_name_key(self):
        """Test that an admin user cannot edit unit name with an invalid key."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_name/1', data=json.dumps(edit_unit_name_key), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid unit_name key')
        assert response.status_code == 400

    def test_edit_existing_unit_name1(self):
        """Test that an admin user cannot edit existing unit name."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_name/1', data=json.dumps(update_existing_unit_name1), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Calculus 1 already exists')
        assert response.status_code == 400

    def test_edit_unexisting_unit2(self):
        """Test that an admin user cannot edit non existing unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_name/100', data=json.dumps(update_unit_name), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404

    def test_edit_unit_code(self):
        """Test that an admin user can edit a unit code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_code/1', data=json.dumps(update_unit_code), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit code updated successfully')
        assert response.status_code == 200

    def test_edit_unit_code_key(self):
        """Test that an admin user cannot edit a unit code with an invalid key."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_code/1', data=json.dumps(edit_unit_code_key), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid unit_code key')
        assert response.status_code == 400

    def test_edit_existing_unit_code1(self):
        """Test that an admin user cannot edit existing unit code."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_code/1', data=json.dumps(update_existing_unit_code1), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'SMA001 already exists')
        assert response.status_code == 400

    def test_edit_unexisting_unit3(self):
        """Test that an admin user cannot edit non existing unit."""
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.put(
            '/api/v1/units/unit_code/100', data=json.dumps(update_unit_code), content_type='application/json',
            headers=self.get_department_head_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Unit not found')
        assert response.status_code == 404
