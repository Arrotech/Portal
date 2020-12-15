import json

from utils.v1.dummy.students_accounts import email_already_exists, new_student_login, new_student_account, wrong_firstname,\
    wrong_lastname, reset_email, reset_unexisting_email, update_student_info, update_student_info_keys,\
    wrong_surname, invalid_student_account_keys, invalid_login_password, admission_already_exists,\
    invalid_email_format, student_invalid_login_email, password_length, new_student_account_invalid_email_format
from .base_test import BaseTest


class TestUsersAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_student_account(self):
        """Test that an admin can add a new student."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_email_format_when_requesting_password_reset_link(self):
        """Test that a user will get an error when they provide an invalid email format when requesting for password rest link."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/reset', data=json.dumps(invalid_email_format), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400

    def test_login_password(self):
        """Test that a user cannot login with an invalid password."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/students/login', data=json.dumps(invalid_login_password), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_get_access_token(self):
        """Test that a user can get the access token using the refresh token."""
        response = self.client.post(
            '/api/v1/users/refresh', content_type='application/json',
            headers=self.get_refresh_token())
        assert response.status_code == 200

    def test_protected_routes(self):
        """Test protected route."""
        response = self.client.get(
            '/api/v1/users/protected', content_type='application/json', headers=self.get_token())
        assert response.status_code == 200

    def test_get_user_by_admission_number(self):
        """Test that a user can get all his/her account informmation with the admission number."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/students/users/NJCF4001', content_type='application/json', headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'successfully retrieved')
        assert response.status_code == 200

    def test_get_user_by_id(self):
        """Test that a user can get all his/her account information with the ID."""
        response = self.client.get(
            '/api/v1/students/users/1', content_type='application/json', headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'successfully retrieved')
        assert response.status_code == 200

    def test_get_non_existing_user_by_id(self):
        """Test get non existing user by id."""
        response = self.client.get(
            '/api/v1/students/users/10', content_type='application/json', headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response.status_code == 404

    def test_the_format_of_create_account_json_keys_for_the_student(self):
        """Test that an admin cannot create a new account for a new student with invalid json keys."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(invalid_student_account_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_password_format(self):
        """Test that the password should be valid."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(password_length), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!')
        assert response.status_code == 400

    def test_email_exists(self):
        """Test that an admin cannot create an account with an exiting email."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(email_already_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Email Already Exists!')
        assert response.status_code == 400

    def test_admission_exists(self):
        """Test that an admin cannot create an account with an exiting admission."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(admission_already_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Admission number Already Exists!')
        assert response.status_code == 400

    def test_student_login(self):
        """Test that students can login to their account."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/students/login', data=json.dumps(new_student_login), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Successfully logged in!')
        assert response.status_code == 200

    def test_password_reset_email_for_the_student(self):
        """Test that a user gets password reset link if they provide valid email."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/reset', data=json.dumps(reset_email), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Check Your Email for the Password Reset Link')
        assert response.status_code == 200

    def test_student_invalid_email_login(self):
        """Test that the student cannot login with an invalid email."""
        response = self.client.post(
            '/api/v1/students/login', data=json.dumps(student_invalid_login_email), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_wrong_firstname(self):
        """Test that an admin cannot register a new student with the wrong firstname format."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(wrong_firstname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'firstname is in wrong format')
        assert response.status_code == 400

    def test_wrong_lastname(self):
        """Test that an admin cannot register a new student with the wrong lastname format."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(wrong_lastname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'lastname is in wrong format')
        assert response.status_code == 400

    def test_wrong_surname(self):
        """Test that an admin cannot register a new student with the wrong surname format."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(wrong_surname), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'surname is in wrong format')
        assert response.status_code == 400

    def test_invalid_email_format(self):
        """Test that an admin cannot register a new student with the wrong email format.."""
        response = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account_invalid_email_format), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400

    def test_invalid_url_path(self):
        """Test when unexisting url is provided."""
        response = self.client.get(
            '/api/v2/party')
        result = json.loads(response.data.decode())
        assert response.status_code == 404
        assert result['message'] == "resource not found"

    def test_send_reset_unexisting_email(self):
        """Test sending a password reset for non existing email."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/reset', data=json.dumps(reset_unexisting_email), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Check Your Email for the Password Reset Link')
        assert response.status_code == 200
