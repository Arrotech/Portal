import json

from utils.v1.dummy.accountant_accounts import admission_already_exists, email_already_exists, new_accountant_account, new_accountant_login, invalid_accountant_account_keys, wrong_firstname,\
    wrong_lastname,\
    wrong_surname, invalid_email_format, password_length, invalid_password, invalid_login_password
from .base_test import BaseTest


class TestUsersAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_accountant_account(self):
        """Test that an admin can create a new account for an accountant."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_login_password(self):
        """Test that a user cannot login with an invalid password."""
        self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(invalid_login_password), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_password_format(self):
        """Test that the password should be valid."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(password_length), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!')
        assert response.status_code == 400

    def test_email_exists(self):
        """Test that an admin cannot create an account with an exiting email."""
        self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(email_already_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Email Already Exists!')
        assert response.status_code == 400

    def test_admission_exists(self):
        """Test that an admin cannot create an account with an exiting admission."""
        self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(admission_already_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Admission number Already Exists!')
        assert response.status_code == 400


    def test_the_format_of_create_account_json_keys_for_the_accountant(self):
        """Test that an admin cannot create a new account with invalid json keys."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(invalid_accountant_account_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_accountant_login(self):
        """Test that students can login to their account."""
        self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(new_accountant_login), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Successfully logged in!')
        assert response.status_code == 200


    def test_accountant_invalid_email_login(self):
        """Test that an admin cannot login with an invalid email."""
        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(invalid_password), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_wrong_firstname(self):
        """Test registering with wrong firstname format."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_firstname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'firstname is in wrong format')
        assert response.status_code == 400

    def test_wrong_lastname(self):
        """Test registering with wrong lastname format."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_lastname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'lastname is in wrong format')
        assert response.status_code == 400

    def test_wrong_surname(self):
        """Test registering with wrong surname format."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_surname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'surname is in wrong format')
        assert response.status_code == 400

    def test_wrong_email(self):
        """Test registering with wrong email format."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(invalid_email_format), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400
