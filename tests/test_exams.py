from tests.base_test import BaseTest
from utils.v1.dummy.academic_year import new_academic_year
from utils.v1.dummy.units import new_unit
from utils.v1.dummy.students_accounts import new_student_account
import json

from utils.v1.dummy.exams import new_entry, invalid_exam_key, invalid_unit_id,\
    update_exam_entry


class TestExams(BaseTest):
    """Test Exams."""

    def test_add_exams(self):
        """Test that an admin can make a new exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Marks added successfully')
        assert response.status_code == 201

    def test_get_exam_by_id(self):
        """Test that an admin can get an exam by id."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/1',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam successfull retrieved')
        assert response.status_code == 200

    def test_get_unexisting_exam_by_id(self):
        """Test that an admin cannot get unexisting exam by id."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/100',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam not found')
        assert response.status_code == 404

    def test_add_exams_keys(self):
        """An admin cannot add an exam with an invalid json key."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_exam_key),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response.status_code == 400

    def test_add_exams_for_non_existing_unit(self):
        """An admin cannot add a exam for a non existing unit"""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(invalid_unit_id),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Unit Calculus 111 not found')
        assert response.status_code == 404

    def test_add_exams_for_non_existing_user(self):
        """An admin cannot make a new exam entry for a non existing user"""
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'],
            'User does not exist or your are trying to enter marks twice')
        assert response.status_code == 400

    def test_add_exams_for_non_existing_year(self):
        """An admin cannot make a new exam entry for non existing year."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Year not found')
        assert response.status_code == 404

    def test_get_exams_by_year_and_admission_no(self):
        """Test that an admin can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/year/NJCF4001/2014-2015',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_exams_aggregate_by_year_and_admission_no(self):
        """Test that s student can view their aggregate."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/aggregate/NJCF4001/2014-2015',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam Total successfull retrieved')
        assert response.status_code == 200

    def test_get_supplementaries_exams_by_year_and_admission_no(self):
        """Test that a student can view their supplementaries by year."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/supplementaries/year/NJCF4001/2014-2015',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_all_supplementaries_exams_by__admission_no(self):
        """Test that a student can view their supplementaries by admission."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/supplementaries/year/all/NJCF4001',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_exams_for_specific_semester(self):
        """Test that an admin can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/year/NJCF4001/2014-2015/1',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_exams_for_a_student_by_admission(self):
        """Test that a student can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/NJCF4001', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_get_total_for_specific_unit(self):
        """Test that an admin can fetch all exams."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/exams/total/NJCF4001/Calculus 1',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exams successfull retrieved')
        assert response.status_code == 200

    def test_update_exams(self):
        """Test that an admin can update an exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/exams/1', data=json.dumps(update_exam_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam updated successfully')
        assert response.status_code == 200

    def test_update_unexisting_exams(self):
        """Test that an admin cannot update an exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/exams/100', data=json.dumps(update_exam_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam not found')
        assert response.status_code == 404

    def test_delete_exams(self):
        """Test that an admin can delete an exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/exams/1',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam deleted successfully')
        assert response.status_code == 200

    def test_delete_unexisting_exams(self):
        """Test that an admin cannot delete an exam entry."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account),
            content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/year', data=json.dumps(new_academic_year),
            content_type='application/json',
            headers=self.get_registrar_token())
        self.client.post(
            '/api/v1/units', data=json.dumps(new_unit),
            content_type='application/json',
            headers=self.get_department_head_token())
        self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/exams/100',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Exam not found')
        assert response.status_code == 404
