import json

from utils.dummy import new_hostel, book_hostel, book_hostel_keys, book_hostel_not_found,\
    book_hostel_user_not_found, new_account
from .base_test import BaseTest


class TestAccommodation(BaseTest):
    """Test accomodation bookings"""

    def test_book_hostel(self):
        """Test that a student can book a hostel."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'],
                         'Hostel booked successfully')
        assert response3.status_code == 201

    def test_book_hostel_keys(self):
        """Test that a student cannot book a hostel with an invalid key."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response3.status_code == 400

    def test_book_hostel_for_non_existing_hostel(self):
        """Test that an existing user cannot book for a non existing hostel."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Hostel not found')
        assert response2.status_code == 404

    def test_book_hostel_for_non_existing_user(self):
        """Test that a non existing user cannot book a hostel."""
        response2 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel_user_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(
            result['message'], 'User does not exist or your are trying to book twice')
        assert response2.status_code == 404

    def test_get_booked_hostels(self):
        """Test that an admin can fetch all booked hostels."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/accommodation', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Hostels retrieved successfully')
        assert response4.status_code == 200

    def test_get_booked_hostel_by_admission(self):
        """Test that a student can view the hostel he/she has booked."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/accommodation/NJCF1001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Hostel retrieved successfully')
        assert response4.status_code == 200

    def test_that_non_existing_user_cannot_view_hostel(self):
        """Test that a student cannot view non existing hostel he/she hasn't booked."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response2 = self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel), content_type='application/json',
            headers=self.get_token())
        response4 = self.client.get(
            '/api/v1/accommodation/NJCF4012', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Hostel not found')
        assert response4.status_code == 404
