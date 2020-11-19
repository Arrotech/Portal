import json

from utils.dummy import add_book, new_account, edit_books, edit_books_keys, add_book_keys
from .base_test import BaseTest


class TestBooks(BaseTest):
    """Test Library."""

    def test_add_books(self):
        """Test that the admin add books."""
        response1 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Book added successfully')
        assert response2.status_code == 201

    def test_add_books_keys(self):
        """Test the add books keys."""
        response1 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response.status_code == 400

    def test_add_books_for_unexisting_user(self):
        """Test that the add books for unexisting user."""
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Student not found')
        assert response.status_code == 404

    def test_get_books(self):
        """Test that an admin can fetch all books that have been added."""
        response2 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/books', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         "Books retrieved successfully")
        assert response1.status_code == 200

    def test_get_books_for_one_student_by_admission(self):
        """Test that a student can fetch all books that were issued."""
        response2 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.get(
            '/api/v1/books/NJCF4001', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Books retrieved successfully')
        assert response1.status_code == 200

    def test_get_books_for_non_existing_user(self):
        """Test that one cannot get books for non existing user"""
        response2 = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.get(
            '/api/v1/books/NJCF1013', content_type='application/json', headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'Student not found')
        assert response3.status_code == 404

    def test_edit_books(self):
        """Test edit books."""
        response1 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Book updated successfully')
        assert response3.status_code == 200

    def test_edit_books_keys(self):
        """Test edit books keys."""
        response1 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books_keys), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Invalid title key')
        assert response2.status_code == 400

    def test_edit_non_existing_book(self):
        """Test edit non existing book."""
        response1 = self.client.post(
            '/api/v1/students/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/books/10', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Book not found')
        assert response2.status_code == 404
