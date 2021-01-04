import json

from utils.v1.dummy.exams import new_entry, invalid_exam_key, invalid_unit_id
from utils.v1.dummy.students_accounts import new_student_account
from utils.v1.dummy.units import new_unit
from utils.v1.dummy.academic_year import new_academic_year
from .base_test import BaseTest


class TestExams(BaseTest):
    """Test Exams."""

    def test_add_exams(self):
        """Test that an admin can make a new exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Marks added successfully')
        assert response.status_code == 201

    def test_add_exams_keys(self):
        """Test that an admin cannot make a new exam entry with an invalid json key."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_exam_key), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response.status_code == 400

    def test_add_exams_for_non_existing_unit(self):
        """Test that an admin cannot make a new exam entry for a non existing unit"""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_unit_id), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Unit Calculus 111 not found')
        assert response.status_code == 404

    def test_add_exams_for_non_existing_user(self):
        """Test that an admin cannot make a new exam entry for a non existing user"""
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'User does not exist or your are trying to enter marks twice')
        assert response.status_code == 400

    def test_add_exams_for_non_existing_year(self):
        """Test that an admin cannot make a new exam entry fro non existing year."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Year not found')
        assert response.status_code == 404

    def test_get_exams_by_year_and_admission_no(self):
        """Test that an admin can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/year/NJCF4001/2014-2015', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_exams_for_specifi_semester(self):
        """Test that an admin can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/year/NJCF4001/2014-2015/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_exams_for_a_student_by_admission(self):
        """Test that a student can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200
