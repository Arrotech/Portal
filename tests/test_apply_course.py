import json

from utils.v1.dummy.apply_course import apply_course, apply_course_keys,\
    apply_course_user_not_found
from utils.v1.dummy.students_accounts import new_student_account
from utils.v1.dummy.courses import new_course
from utils.v1.dummy.campuses import new_campus
from utils.v1.dummy.certificates import new_certificate
from utils.v1.dummy.institutions import new_institution
from utils.v1.dummy.departments import new_department
from .base_test import BaseTest


class TestApplyCourse(BaseTest):
    """Test apply course endpoints."""

    def test_apply_course(self):
        """Test that a student can apply a course."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        print(response)
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Course applied successfully')
        assert response.status_code == 201

    def test_apply_course_keys(self):
        """Test that a student cannot apply a course with an invalid json key."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid admission_no key')
        assert response.status_code == 400

    def test_apply_course_user_not_found(self):
        """Test that a student cannot apply a course if they dont exists."""
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_user_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Student not found')
        assert response.status_code == 404

    def test_apply_course_campus_not_found(self):
        """Test that a student cannot apply a course if the campus doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Campus not found')
        assert response.status_code == 404

    def test_apply_course_certificate_not_found(self):
        """Test that a student cannot apply a course if the certificate doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Certificate not found')
        assert response.status_code == 404

    def test_apply_course_department_not_found(self):
        """Test that a student cannot apply a course if the department doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response.status_code == 404

    def test_apply_course_not_found(self):
        """Test that a student cannot apply a course if the course doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response.status_code == 404

    def test_apply_course_institution_not_found(self):
        """Test that a student cannot apply a course if the course doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Institution not found')
        assert response.status_code == 404

    def test_apply_course_get_course_by_id(self):
        """Test that a student can fetch course by id."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/apply_course/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Course retrieved successfully')
        assert response.status_code == 200

    def test_apply_course_get_non_exisiting_course_by_id(self):
        """Test that a student cannot fetch course by id if doesn't exists."""
        self.client.post(
            '/api/v1/students/register', data=json.dumps(new_student_account), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/institutions', data=json.dumps(new_institution), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/campuses', data=json.dumps(new_campus), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/certificates', data=json.dumps(new_certificate), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        response = self.client.get(
            '/api/v1/apply_course/10', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response.status_code == 404
