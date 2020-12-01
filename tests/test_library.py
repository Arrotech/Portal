import json

from utils.v1.dummy.library import add_book, edit_books, edit_books_keys, add_book_keys
from utils.v1.dummy.students_accounts import new_student_account
from .base_test import BaseTest


class TestBooks(BaseTest):
    """Test Library."""

    def test_add_books(self):
        """Test that the admin add books."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Book added successfully')
        assert response.status_code == 201

    def test_add_books_keys(self):
        """Test the add books keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response.status_code == 400

    # def test_add_books_for_unexisting_user(self):
    #     """Test that the add books for unexisting user."""
    #     response = self.client.post(
    #         '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
    #         headers=self.get_admin_token())
    #     result = json.loads(response.data.decode())
    #     self.assertEqual(result['message'], 'Student not found')
    #     assert response.status_code == 404

    def test_get_books(self):
        """Test that an admin can fetch all books that have been added."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/books', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         "Books retrieved successfully")
        assert response.status_code == 200

    def test_get_books_for_one_student_by_admission(self):
        """Test that a student can fetch all books that were issued."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/books/NJCF4001', content_type='application/json', headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Books retrieved successfully')
        assert response.status_code == 200

    # def test_get_books_for_non_existing_user(self):
    #     """Test that one cannot get books for non existing user"""
    #     self.client.post(
    #         '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
    #         headers=self.get_admin_token())
    #     response = self.client.get(
    #         '/api/v1/books/NJCF1013', content_type='application/json', headers=self.get_token())
    #     result = json.loads(response.data.decode())
    #     self.assertEqual(result['message'],
    #                      'Student not found')
    #     assert response.status_code == 404

    def test_edit_books(self):
        """Test edit books."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Book updated successfully')
        assert response.status_code == 200

    def test_edit_books_keys(self):
        """Test edit books keys."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/books/1', data=json.dumps(edit_books_keys), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid title key')
        assert response.status_code == 400

    def test_edit_non_existing_book(self):
        """Test edit non existing book."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/books/10', data=json.dumps(edit_books), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Book not found')
        assert response.status_code == 404
