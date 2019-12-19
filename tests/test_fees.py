import json

from utils.dummy import add_fees, new_account, bursar_account_test
from .base_test import BaseTest


class TestFees(BaseTest):
    """Test Fees."""
    def test_add_fees(self):
        """Test that the add fees endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Entry made successsfully')
        assert response.status_code == 201

    def test_add_fees_for_unexisting_student(self):
        """Test that the add fees endpoint works."""
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student with that Admission Number does not exitst.')
        assert response.status_code == 404

    def test_get_fees(self):
        """Test fetching all fees that have been created."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response2 = self.client.get(
            '/api/v1/fees', content_type='application/json', headers=self.get_bursar_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response2.status_code == 200

    def test_get_fees_by_admission(self):
        """Test fetching all fees that have been created."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees), content_type='application/json',
            headers=self.get_bursar_token())
        response2 = self.client.get(
            '/api/v1/fees/NJCF4001', content_type='application/json', headers=self.get_bursar_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response2.status_code == 200

    def test_get_unexisting_fee(self):
        """Test getting unexisting specific fee by admission_no."""

        response1 = self.client.get(
            '/api/v1/fees/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Fees Not Found')
        assert response1.status_code == 404