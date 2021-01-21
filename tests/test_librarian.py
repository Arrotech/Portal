import json

from utils.v1.dummy.librarian import admission_already_exists,\
    email_already_exists, new_librarian_account,\
    invalid_admin_account_keys, wrong_firstname,\
    wrong_lastname, wrong_surname, invalid_email_format, password_length
from tests.base_test import BaseTest


class TestLibrarianAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_librarian_account(self):
        """Test that an admin can create a new account."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(new_librarian_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_invalid_email_format(self):
        """An admin cannot add a student with the wrong email format.."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(invalid_email_format),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid Email Format!')
        assert response.status_code == 400

    def test_password_format(self):
        """Test that the password should be valid."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(password_length),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Invalid password')
        assert response.status_code == 400

    def test_email_exists(self):
        """An admin cannot create an account with an exiting email."""
        self.client.post(
            '/api/v1/library/register', data=json.dumps(new_librarian_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(email_already_exists),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Email Already Exists!')
        assert response.status_code == 400

    def test_admission_exists(self):
        """An admin cannot create an account with an exiting admission."""
        self.client.post(
            '/api/v1/library/register', data=json.dumps(new_librarian_account),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/library/register',
            data=json.dumps(admission_already_exists),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Admission number Already Exists!')
        assert response.status_code == 400

    def test_the_format_of_create_account_json_keys_for_the_registrar(self):
        """An admin cannot create a new account with invalid json keys."""
        response = self.client.post(
            '/api/v1/library/register',
            data=json.dumps(invalid_admin_account_keys),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid firstname key')
        assert response.status_code == 400

    def test_wrong_firstname(self):
        """Test registering with wrong firstname format."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(wrong_firstname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'firstname is in wrong format')
        assert response.status_code == 400

    def test_wrong_lastname(self):
        """Test registering with wrong lastname format."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(wrong_lastname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'lastname is in wrong format')
        assert response.status_code == 400

    def test_wrong_surname(self):
        """Test registering with wrong surname format."""
        response = self.client.post(
            '/api/v1/library/register', data=json.dumps(wrong_surname),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'surname is in wrong format')
        assert response.status_code == 400
