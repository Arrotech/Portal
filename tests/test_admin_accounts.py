import json

from utils.v1.dummy.admin_accounts import admission_already_exists,\
    email_already_exists, new_admin_account, new_admin_login,\
    invalid_admin_account_keys, wrong_firstname, wrong_lastname,\
    wrong_surname, invalid_email_format, password_length,\
    invalid_login_password, staff_invalid_login_email
from utils.v1.dummy.students_accounts import new_student_account,\
    update_student_info, update_student_info_keys
from tests.base_test import BaseTest


class TestUsersAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_admin_account(self):
        """Test that an admin can create a new account."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_invalid_login_password(self):
        """Test that a user cannot login with an invalid password."""
        self.client.post(
            '/api/v1/staff/register',
            data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/login',
            data=json.dumps(invalid_login_password),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_get_users(self):
        """Test that an admin can fetch all users."""
        response = self.client.get(
            '/api/v1/staff/users', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response.status_code == 200

    def test_get_total_number_of_students(self):
        """An admin can fetch the total number of his/her students."""
        response = self.client.get(
            '/api/v1/staff/students/student', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response.status_code == 200

    def test_get_grouped_users(self):
        """Test that an admin can fetch users by their roles."""
        response = self.client.get(
            '/api/v1/staff/users/admin', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response.status_code == 200

    def test_password_format(self):
        """Test that the password should be valid."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(password_length),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Invalid password')
        assert response.status_code == 400

    def test_email_exists(self):
        """An admin cannot create an account with an exiting email."""
        self.client.post(
            '/api/v1/staff/register', data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(email_already_exists),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Email Already Exists!')
        assert response.status_code == 400

    def test_admission_exists(self):
        """An admin cannot create an account with an exiting admission."""
        self.client.post(
            '/api/v1/staff/register', data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/register',
            data=json.dumps(admission_already_exists),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Admission number Already Exists!')
        assert response.status_code == 400

    def test_the_format_of_create_account_json_keys_for_the_admin(self):
        """An admin cannot create a new account with invalid json keys."""
        response = self.client.post(
            '/api/v1/staff/register',
            data=json.dumps(invalid_admin_account_keys),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_staff_login(self):
        """Test that students can login to their account."""
        self.client.post(
            '/api/v1/staff/register', data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/login', data=json.dumps(new_admin_login),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Successfully logged in!')
        assert response.status_code == 200

    def test_staff_invalid_email_login(self):
        """Test that an admin cannot login with an invalid email."""
        response = self.client.post(
            '/api/v1/staff/login', data=json.dumps(staff_invalid_login_email),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_fresh_staff_login(self):
        """Test that accountants can login to their account again."""
        self.client.post(
            '/api/v1/staff/register',
            data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/fresh-login', data=json.dumps(new_admin_login),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Successfully logged in!')
        assert response.status_code == 200

    def test_fresh_staff_invalid_email_login(self):
        """Test that an admin cannot login with an invalid email."""
        response = self.client.post(
            '/api/v1/staff/fresh-login', data=json.dumps(staff_invalid_login_email),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_fresh_login_password(self):
        """Test that a user cannot login with an invalid password."""
        self.client.post(
            '/api/v1/staff/register',
            data=json.dumps(new_admin_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/staff/fresh-login',
            data=json.dumps(invalid_login_password),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email or Password')
        assert response.status_code == 401

    def test_wrong_firstname(self):
        """Test registering with wrong firstname format."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(wrong_firstname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'firstname is in wrong format')
        assert response.status_code == 400

    def test_wrong_lastname(self):
        """Test registering with wrong lastname format."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(wrong_lastname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'lastname is in wrong format')
        assert response.status_code == 400

    def test_wrong_surname(self):
        """Test registering with wrong surname format."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(wrong_surname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'surname is in wrong format')
        assert response.status_code == 400

    def test_wrong_email(self):
        """Test registering with wrong email format."""
        response = self.client.post(
            '/api/v1/staff/register', data=json.dumps(invalid_email_format),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400

    def test_update_student_info(self):
        """Test that an admin can update their information"""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/user/update/NJCF4001',
            data=json.dumps(update_student_info),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User updated successfully')
        assert response.status_code == 200

    def test_update_student_info_json_keys(self):
        """An admin cannot update their information with invalid json keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/user/update/NJCF4001',
            data=json.dumps(update_student_info_keys),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_update_student_info_for_non_existing_student(self):
        """An admin cannot update their information with unexisting account."""
        response = self.client.put(
            '/api/v1/user/update/100', data=json.dumps(update_student_info),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'User not found')
        assert response.status_code == 404
