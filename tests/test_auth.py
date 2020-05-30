import json

from utils.dummy import admin_login, admin_account_test, admin_account, email_already_exists, Invalid_register_key, create_account, user_login, new_account, new_login, new_account1, wrong_firstname,\
    wrong_lastname, reset_email, reset_unexisting_email, update_user_password, update_user_info, update_user_info_keys, promote_user, promote_user_key, wrong_student_email_token, student_email_token,\
    wrong_surname, wrong_email, password_length, invalid_password, wrong_role, wrong_account_keys, wrong_password_login,\
    password_reset_invalid_email_format, reset_password
from .base_test import BaseTest


class TestUsersAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_account(self):
        """Test that the user can create a new account."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_forgot_password_invalid_email_format(self):
        """Test that a user will get an error message why they provide invalid email format."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/auth/forgot', data=json.dumps(password_reset_invalid_email_format), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response1.status_code == 400

    def test_promote_user(self):
        """Test promote user."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.put(
            '/api/v1/auth/users/NJCF4001/promote', data=json.dumps(promote_user), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'student promoted successfully')
        assert response1.status_code == 200

    def test_promote_user_unexisting_user(self):
        """Test promote non existing user."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.put(
            '/api/v1/auth/users/NJCF4002/promote', data=json.dumps(promote_user), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'student not found')
        assert response1.status_code == 404

    def test_login_with_wrong_password(self):
        """Test login with wrong password."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/auth/login', data=json.dumps(wrong_password_login), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response1.status_code == 401

    def test_refresh_token(self):
        """Test refresh token."""
        response = self.client.post(
            '/api/v1/auth/refresh', content_type='application/json',
            headers=self.get_refresh_token())
        assert response.status_code == 200

    def test_protected(self):
        """Test protected route."""
        response = self.client.post(
            '/api/v1/auth/register', content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/auth/protected', content_type='application/json', headers=self.get_token())
        assert response1.status_code == 200

    def test_get_users(self):
        """Test fetching all users."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/auth/users', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response1.status_code == 200

    def test_get_user_by_admission_no(self):
        """Test getting a user by admission."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/auth/users/NJCF4001', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'successfully retrieved')
        assert response1.status_code == 200

    def test_get_user_by_id(self):
        """Test get user by id."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/auth/users/1', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'successfully retrieved')
        assert response1.status_code == 200

    def test_get_non_existing_user_by_id(self):
        """Test get non existing user by id."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/auth/users/10', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response1.status_code == 404

    def test_create_account_keys(self):
        """Test register user with invalid json keys."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_promote_user_keys(self):
        """Test the promote user with invalid json keys."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.put(
            '/api/v1/auth/users/NJCF4001/promote', data=json.dumps(promote_user_key), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Invalid current_year key')
        assert response1.status_code == 400

    def test_password_length(self):
        """Test password length."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(password_length), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!')
        assert response.status_code == 400

    def test_email_exists(self):
        """Test registering with existing email."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(email_already_exists), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Email Already Exists!')
        assert response.status_code == 400

    def test_Invalid_register_key(self):
        """Test registering with invalid json keys."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(Invalid_register_key), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_login(self):
        """Test user login."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account1), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(new_login), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Successfully logged in!')
        assert response.status_code == 200

    def test_forgot_password(self):
        """Test reset password email."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account1), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/auth/forgot', data=json.dumps(student_email_token), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Check Your Email for the Password Reset Link')
        assert response.status_code == 200

    def test_invalid_email_login(self):
        """Test login with non existing email."""
        response = self.client.post(
            '/api/v1/auth/login', data=json.dumps(new_login), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_wrong_firstname(self):
        """Test registering with wrong firstname format."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_firstname), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'firstname is in wrong format')
        assert response.status_code == 400

    def test_wrong_lastname(self):
        """Test registering with wrong lastname format."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_lastname), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'lastname is in wrong format')
        assert response.status_code == 400

    def test_wrong_surname(self):
        """Test registering with wrong surname format."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_surname), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'surname is in wrong format')
        assert response.status_code == 400

    def test_wrong_email(self):
        """Test registering with wrong email format."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_email), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400

    def test_unexisting_register_ur(self):
        """Test when unexisting url is provided."""
        response = self.client.get(
            '/api/v2/party')
        result = json.loads(response.data.decode())
        assert response.status_code == 404
        assert result['message'] == "resource not found"

    def test_update_user_info(self):
        """Test that a user can update their information"""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.put(
            '/api/v1/auth/users/user_info/NJCF4001', data=json.dumps(update_user_info), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'User updated successfully')
        assert response2.status_code == 200

    def test_update_user_info_keys(self):
        """Test that a user cannot update their information with invalid json keys."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.put(
            '/api/v1/auth/users/user_info/1', data=json.dumps(update_user_info_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response2.status_code == 400

    def test_update_user_info_for_non_existing_user(self):
        """Test that a user cannot update their information for non existing user."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.put(
            '/api/v1/auth/users/user_info/100', data=json.dumps(update_user_info), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response2.status_code == 404

    def test_send_reset_email(self):
        """Test sending a password reset email."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/auth/forgot', data=json.dumps(reset_email), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Check Your Email for the Password Reset Link')
        assert response2.status_code == 200

    def test_send_reset_unexisting_email(self):
        """Test sending a password reset for non existing email."""
        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/auth/forgot', data=json.dumps(reset_unexisting_email), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Check Your Email for the Password Reset Link')
        assert response2.status_code == 200
