import json

from utils.v1.dummy.accommodation import book_hostel, book_hostel_keys,\
    update_accommodation
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

    def test_get_booked_hostel_by_id(self):
        """Test that a student can view the hostel he/she has booked by id."""
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
            '/api/v1/accommodation/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel retrieved successfully')
        assert response.status_code == 200

    def test_get_unexisting_hostel_by_id(self):
        """Test that a student cannot view unexisting hostel by id."""
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
            '/api/v1/accommodation/100', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel not found')
        assert response.status_code == 404

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

    def test_get_booked_hostels_history(self):
        """Test that a student can view all the hostels he/she has booked."""
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
            '/api/v1/accommodation/all/NJCF4001',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Accomodation history retrieved successfully')
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

    def test_update_accommodation(self):
        """Test that a student can update accommodation information."""
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
        response = self.client.put(
            '/api/v1/accommodation/1', data=json.dumps(update_accommodation),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel accommodation updated successfully')
        assert response.status_code == 200

    def test_update_unexisting_accommodation(self):
        """Test that a student cannot update unexisting accommodation."""
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
        response = self.client.put(
            '/api/v1/accommodation/100', data=json.dumps(update_accommodation),
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel accommodation not found')
        assert response.status_code == 404

    def test_delete_accommodation(self):
        """Test that a student can delete accommodation."""
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
        response = self.client.delete(
            '/api/v1/accommodation/1',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel accommodation deleted successfully')
        assert response.status_code == 200

    def test_delete_unexisting_accommodation(self):
        """Test that a student cannot delete unexisting accommodation."""
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
        response = self.client.delete(
            '/api/v1/accommodation/100',
            content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Hostel accommodation not found')
        assert response.status_code == 404
