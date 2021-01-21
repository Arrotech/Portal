import json

from utils.v1.dummy.accommodation import book_hostel, book_hostel_keys
from utils.v1.dummy.hostels import new_hostel
from utils.v1.dummy.students_accounts import new_student_account
from tests.base_test import BaseTest


class TestAccommodation(BaseTest):
    """Test accomodation bookings"""

    def test_book_hostel(self):
        """Test that a student can book a hostel."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        response = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel booked successfully')
        assert response.status_code == 201

    def test_book_hostel_keys(self):
        """Test that a student cannot book a hostel with an invalid key."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        response = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel_keys),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid admission_no key')
        assert response.status_code == 400

    def test_book_hostel_for_non_existing_hostel(self):
        """Test that an existing user cannot book for a non existing hostel."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Hostel not found')
        assert response.status_code == 404

    def test_book_hostel_for_non_existing_user(self):
        """Test that a non existing user cannot book a hostel."""
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        response = self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'User not found')
        assert response.status_code == 404

    def test_get_booked_hostels(self):
        """Test that an admin can fetch all booked hostels."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/accommodation', content_type='application/json',
            headers=self.get_hostel_manager_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostels retrieved successfully')
        assert response.status_code == 200

    def test_get_booked_hostel_by_admission(self):
        """Test that a student can view the hostel he/she has booked."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/accommodation/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel retrieved successfully')
        assert response.status_code == 200

    def test_that_non_existing_user_cannot_view_hostel(self):
        """A student cannot view non existing hostel he/she hasn't booked."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/hostels', data=json.dumps(new_hostel),
            content_type='application/json',
            headers=self.get_hostel_manager_token())
        self.client.post(
            '/api/v1/accommodation', data=json.dumps(book_hostel),
            content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/accommodation/NJCF4012', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel not found')
        assert response.status_code == 404
