import json

from utils.dummy import new_accountant_account, wrong_accountant_account_keys, wrong_accountant_account_firstname,\
    wrong_accountant_account_lastname,\
    wrong_accountant_account_email, invalid_accountant_password,\
    wrong_accountant_account_password, username_accountant_exists,\
    email_accountant_exists, wrong_accountant_login_keys, wrong_accountant_password_login, wrong_accountant_email_login, invalid_accountant_email_password
from .base_test import BaseTest


class TestAccountantAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_account(self):
        """Test when a new user creates a new account."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_get_users(self):
        """Test get all users."""
        response1 = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        response = self.client.get(
            '/api/v1/accountant/users', content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'success')
        assert response.status_code == 200

    def test_get_user(self):
        """Test get a user by username."""
        response1 = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        response = self.client.get(
            '/api/v1/accountant/users/Arrotech', content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'success')
        assert response.status_code == 200

    def test_get_unexisting_user(self):
        """Test getting unexisting user."""
        response = self.client.get(
            '/api/v1/accountant/users/Omondi', content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response.status_code == 404

    def test_create_account_keys(self):
        """Test create account json keys."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_accountant_account_keys), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid username key')
        assert response.status_code == 400

    def test_account_firstname_input(self):
        """Test create account first name input."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_accountant_account_firstname), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'First name is in wrong format')
        assert response.status_code == 400

    def test_account_lastname_input(self):
        """Test create account last name input."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_accountant_account_lastname), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Last name is in wrong format')
        assert response.status_code == 400

    def test_account_email_input(self):
        """Test create account email input."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_accountant_account_email), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid email!')
        assert response.status_code == 400

    def test_account_password_input(self):
        """Test create account password input."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(wrong_accountant_account_password), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!')
        assert response.status_code == 400

    def test_create_account_with_an_existing_username(self):
        """Test when a new user creates a new account with an existing username."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        response1 = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(username_accountant_exists), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Username already exists!')
        assert response1.status_code == 400

    def test_create_account_with_an_existing_email(self):
        """Test when a new user creates a new account with an existing email."""
        response = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        response1 = self.client.post(
            '/api/v1/accountant/register', data=json.dumps(email_accountant_exists), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Email already exists!')
        assert response1.status_code == 400

    def test_login_keys(self):
        """Test login json keys."""
        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(wrong_accountant_login_keys), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid email key')
        assert response.status_code == 400

    def test_login_with_wrong_email(self):
        """Test login with wrong email."""
        response1 = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(wrong_accountant_email_login), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response1.status_code == 401

    def test_refresh_token(self):
        """Test refresh token endpoint."""
        response = self.client.post(
            '/api/v1/accountant/refresh', content_type='application/json',
            headers=self.get_accountant_refresh_token())
        assert response.status_code == 200

    def test_protected(self):
        """Test protect route."""
        response = self.client.post(
            '/api/v1/accountant/register', content_type='application/json',
            headers=self.get_bursar_token())
        response1 = self.client.get(
            '/api/v1/accountant/protected', content_type='application/json', headers=self.get_token())
        assert response1.status_code == 200

    def test_method_not_allowed(self):
        """Test method not allowed."""
        response = self.client.get(
            '/api/v1/accountant/register', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'method not allowed')
        assert response.status_code == 405

    def test_invalid_email_login(self):
        """Test the vote json keys."""

        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(invalid_accountant_email_password), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_invalid_login_password(self):
        """Test the vote json keys."""

        response = self.client.post(
            '/api/v1/accountant/login', data=json.dumps(invalid_accountant_password), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')

    def test_unexisting_Url(self):
        """Test when unexisting url is provided."""
        response = self.client.post(
            '/api/v1/accountant/registe', data=json.dumps(new_accountant_account), content_type='application/json',
            headers=self.get_bursar_token())
        result = json.loads(response.data.decode())
        assert response.status_code == 404
        assert result['message'] == "resource not found"
