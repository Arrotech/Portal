import json

from utils.dummy import add_book, new_account, edit_books, edit_books_keys, add_book_keys
from .base_test import BaseTest


class TestBooks(BaseTest):
    """Test Library."""
    def test_add_books(self):
        """Test that the add books endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Book awarded successfully')
        assert response.status_code == 201

    def test_add_books_keys(self):
        """Test the add books keys."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid form key')
        assert response.status_code == 400

    def test_add_books_for_unexisting_user(self):
        """Test that the add books for unexisting user."""
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student with that Admission Number does not exitst.')
        assert response.status_code == 404

    def test_get_books(self):
        """Test fetching all books that have been created."""
        response2 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/books', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         "Retrieved successfully")
        assert response1.status_code == 200

    def test_get_book(self):
        """Test getting a specific book by admission_no."""
        response2 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/books/NJCF4001', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Retrieved successfully')
        assert response1.status_code == 200

    def test_get_unexisting_book(self):
        """Test getting unexisting specific book by admission_no."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.get(
            '/api/v1/books/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Book Not Found')
        assert response1.status_code == 404

    def test_edit_books(self):
        """Test edit books."""

        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'book updated successfully')
        assert response2.status_code == 200

    def test_edit_books_keys(self):
        """Test edit books keys."""

        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books_keys), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Invalid form key')
        assert response2.status_code == 400

    def test_edit_unexisting_fees(self):
        """Test edit unexisting fees."""

        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/books/1000', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'book not found')
        assert response2.status_code == 404
