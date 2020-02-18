import json

from utils.dummy import greater_than, less_than, entry, new_entry, edit_exams, new_account, wrong_exam_keys, admin_account_test, term_restrictions, form_restrictions, type_restrictions, edit_exams_keys
from .base_test import BaseTest


class TestExams(BaseTest):
    """Test exams."""

    def test_add_exams(self):
        """Test that the add exams endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Entry created successfully!')
        assert response.status_code == 201

    def test_marks_less_than_0(self):
        """Test that the add exams endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(less_than), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Please add a number greater than 0')
        assert response.status_code == 400

    def test_marks_greater_than_100(self):
        """Test that the add exams endpoint works."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(greater_than), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Please add a number less than 100')
        assert response.status_code == 400

    def test_exam_keys(self):
        """Test the vote json keys."""

        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(wrong_exam_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid maths key')
        assert response.status_code == 400

    def test_add_exams_with_unexisting_user(self):
        """Test that the add exams endpoint works."""
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'Student with that Admission Number does not exitst.')
        assert response.status_code == 404

    def test_get_exams(self):
        """Test fetching all exams that have been created."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/exams', content_type='application/json', headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], "successfully retrieved")
        assert response2.status_code == 200

    def test_get_exam_by_admission_no(self):
        """Test getting a specific party by id."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/exams/NJCF4001', content_type='application/json', headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'successfully retrieved')
        assert response2.status_code == 200

    def test_get_unexisting_exam(self):
        """Test getting unexisting specific exam by admission_no."""
        response1 = self.client.get(
            '/api/v1/exams/NJCF4057', content_type='application/json', headers=self.get_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Exam Not Found')
        assert response1.status_code == 404

    def test_unexisting_exams_url(self):
        """Test when unexisting url is provided."""
        response = self.client.get(
            '/api/v1/exam', headers=self.get_token())
        result = json.loads(response.data.decode())
        assert response.status_code == 404
        assert result['message'] == "resource not found"

    def test_method_not_allowed(self):
        """Test method not allowed."""
        response = self.client.put(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'method not allowed')
        assert response.status_code == 405

    def test_delete_exams(self):
        """Test deleting a specific exam."""
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.delete(
            '/api/v1/exams/NJCF4001', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Exam deleted successfully')
        assert response1.status_code == 200

    def test_delete_unexisting_exams(self):
        """Test deleting unexisting exam."""
        response1 = self.client.delete(
            '/api/v1/exams/NJCF4057', content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Exam not found')
        assert response1.status_code == 404

    def test_edit_exams(self):
        """Test edit exams."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/exams/1', data=json.dumps(edit_exams), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'exam updated successfully')
        assert response2.status_code == 200

    def test_edit_exams_keys(self):
        """Test edit exams keys."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/exams/1', data=json.dumps(edit_exams_keys), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Invalid maths key')
        assert response2.status_code == 400

    def test_edit_unexisting_exams(self):
        """Test edit unexisting exams."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json',
            headers=self.get_token())
        response1 = self.client.post(
            '/api/v1/exams', data=json.dumps(new_entry), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.put(
            '/api/v1/exams/1000', data=json.dumps(edit_exams), content_type='application/json', headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'exam not found')
        assert response2.status_code == 404
