import json

from utils.dummy import apply_course, apply_course_department_not_found, apply_course_keys,\
    apply_course_not_found, apply_course_user_not_found, new_department, new_course
from .base_test import BaseTest


class TestApplyCourse(BaseTest):
    """Test apply course endpoints."""

    def test_apply_course(self):
        """Test that a student can apply a course."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Course applied successfully')
        assert response4.status_code == 201

    def test_apply_course_keys(self):
        """Test that a student cannot apply a course with an invalid json key."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_keys), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Invalid user_id key')
        assert response4.status_code == 400

    def test_apply_course_user_not_found(self):
        """Test that a student cannot apply a course if they dont exists."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_user_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'User not found')
        assert response4.status_code == 404

    def test_apply_course_department_not_found(self):
        """Test that a student cannot apply a course if the department doesn't exists."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_department_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response4.status_code == 404

    def test_apply_course_not_found(self):
        """Test that a student cannot apply a course if the course doesn't exists."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course_not_found), content_type='application/json',
            headers=self.get_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response4.status_code == 404

    def test_apply_course_get_course_by_id(self):
        """Test that a student can fetch course by id."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        response5 = self.client.get(
            '/api/v1/apply_course/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Course retrieved successfully')
        assert response5.status_code == 200

    def test_apply_course_get_non_exisiting_course_by_id(self):
        """Test that a student cannot fetch course by id if doesn't exists."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/apply_course', data=json.dumps(apply_course), content_type='application/json',
            headers=self.get_token())
        response5 = self.client.get(
            '/api/v1/apply_course/10', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'Course not found')
        assert response5.status_code == 404
