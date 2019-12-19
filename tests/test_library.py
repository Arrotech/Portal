import json

from utils.dummy import add_book
from .base_test import BaseTest


class TestBooks(BaseTest):
    """Test Library."""
    def test_add_books(self):
        """Test that the add books endpoint works."""
        response = self.client.post(
            '/api/v1/books', data=json.dumps(add_book), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Book awarded successfully')
        assert response.status_code == 201

    def test_get_books(self):
        """Test fetching all books that have been created."""
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

        response1 = self.client.get(
            '/api/v1/books/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Book Not Found')
        assert response1.status_code == 404
