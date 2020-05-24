import json

from utils.dummy import add_fees, new_account, bursar_account_test, edit_fees, add_fees_keys, edit_fees_keys
from .base_test import BaseTest


class TestFees(BaseTest):
    """Test Fees."""

    def test_add_fees(self):
        """Test that the add fees endpoint works."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Entry made successfully')
        assert response2.status_code == 201

    def test_add_fees_keys(self):
        """Test that the bursar cannot add fees with invalid json keys."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees_keys), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response2.status_code == 400

    def test_add_fees_for_unexisting_student(self):
        """Test that bursar cannot add fees for non existing student."""
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student not found')
        assert response.status_code == 404

    def test_get_fees(self):
        """Test fetch all fees.."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response2 = self.client.get(
            '/api/v1/fees', content_type='application/json', headers=self.get_bursar_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], "Fees retrieved successfully")
        assert response2.status_code == 200

    def test_get_fees_by_user_id(self):
        """Test fetching all fees by user id."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response2 = self.client.get(
            '/api/v1/fees/NJCF1001', content_type='application/json', headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], "Fees retrieved successfully")
        assert response2.status_code == 200

    def test_get_fees_for_non_existing_student(self):
        """Test getting fees for a non existing student."""
        response1 = self.client.get(
            '/api/v1/fees/NJCF1012', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Student not found')
        assert response1.status_code == 404

    def test_edit_fees(self):
        """Test edit fees."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response3 = self.client.put(
            '/api/v1/fees/1', data=json.dumps(edit_fees), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Fees updated successfully')
        assert response3.status_code == 200

    def test_edit_fees_keys(self):
        """Test edit fees keys."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response3 = self.client.put(
            '/api/v1/fees/1', data=json.dumps(edit_fees_keys), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Invalid transaction_type key')
        assert response3.status_code == 400

    def test_edit_unexisting_fees(self):
        """Test edit unexisting fees."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response3 = self.client.put(
            '/api/v1/fees/10', data=json.dumps(edit_fees), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Fees not found')
        assert response3.status_code == 404
