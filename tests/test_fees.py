import json

from utils.v1.dummy.fees import add_fees, edit_fees, add_fees_keys,\
    edit_fees_keys
from utils.v1.dummy.students_accounts import new_student_account
from tests.base_test import BaseTest


class TestFees(BaseTest):
    """Test Fees."""

    def test_add_fees(self):
        """Test that the add fees endpoint works."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Entry made successfully')
        assert response.status_code == 201

    def test_add_fees_keys(self):
        """Test that the bursar cannot add fees with invalid json keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees_keys),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response.status_code == 400

    def test_add_fees_for_unexisting_student(self):
        """Test that bursar cannot add fees for non existing student."""
        response = self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student not found')
        assert response.status_code == 404

    def test_get_fees(self):
        """Test fetch all fees.."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.get(
            '/api/v1/fees', content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Fees retrieved successfully")
        assert response.status_code == 200

    def test_get_fees_by_admission(self):
        """Test fetching all fees by user id."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.get(
            '/api/v1/fees/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Fees retrieved successfully")
        assert response.status_code == 200

    def test_get_latest_fees_by_admission(self):
        """Test fetching latest fee by admission."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.get(
            '/api/v1/fees/latest/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Fee retrieved successfully")
        assert response.status_code == 200

    def test_get_fee_balance_by_admission(self):
        """Test fetching fee balance by admission."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.get(
            '/api/v1/fees/balance/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Fee retrieved successfully")
        assert response.status_code == 200

    def test_get_fees_by_id(self):
        """Test fetching fees by id."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.get(
            '/api/v1/fees/1', content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "Fee retrieved successfully")
        assert response.status_code == 200

    def test_get_fees_for_non_existing_student(self):
        """Test getting fees for a non existing student."""
        response = self.client.get(
            '/api/v1/fees/NJCF1012', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student not found')
        assert response.status_code == 404

    def test_get_fees_for_non_existing_id(self):
        """Test getting fees for a non existing student."""
        response = self.client.get(
            '/api/v1/fees/100', content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Fee not found')
        assert response.status_code == 404

    def test_edit_fees(self):
        """Test edit fees."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.put(
            '/api/v1/fees/1', data=json.dumps(edit_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Fees updated successfully')
        assert response.status_code == 200

    def test_edit_fees_keys(self):
        """Test edit fees keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.put(
            '/api/v1/fees/1', data=json.dumps(edit_fees_keys),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid transaction_type key')
        assert response.status_code == 400

    def test_edit_unexisting_fees(self):
        """Test edit unexisting fees."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.put(
            '/api/v1/fees/10', data=json.dumps(edit_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Fees not found')
        assert response.status_code == 404

    def test_delete_fees(self):
        """Test delete fees."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.delete(
            '/api/v1/fees/1',
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Fee deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_fees(self):
        """Test delete non-existing fees."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/fees', data=json.dumps(add_fees),
            content_type='application/json',
            headers=self.get_accountant_token())
        response = self.client.delete(
            '/api/v1/fees/100',
            content_type='application/json',
            headers=self.get_accountant_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Fee not found')
        assert response.status_code == 404
