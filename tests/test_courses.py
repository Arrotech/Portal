import json

from utils.dummy import new_course, new_department, add_course_keys, add_non_exisitng_department,\
    course_name_exists, add_department
from .base_test import BaseTest


class TestCourses(BaseTest):
    """Test courses."""

    def test_add_course(self):
        """Test that admin can add a course."""
        response = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'maths and computer science added successfully')
        assert response1.status_code == 201

    def test_add_course_keys(self):
        """Test that an admin cannot add a course with an invalid key."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(add_course_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response3.data.decode())
        self.assertEqual(result['message'], 'Invalid course_name key')
        assert response3.status_code == 400

    def test_add_course_for_non_existing_department(self):
        """Test that an admin cannot add a course for non existing department."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/courses', data=json.dumps(add_non_exisitng_department), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response4.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response4.status_code == 404
        
    def test_add_course_for_already_existing_course_name(self):
        """Test that an admin cannot add a course for non existing department."""
        response2 = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response3 = self.client.post(
            '/api/v1/departments', data=json.dumps(add_department), content_type='application/json',
            headers=self.get_admin_token())
        response4 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response5 = self.client.post(
            '/api/v1/courses', data=json.dumps(course_name_exists), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response5.data.decode())
        self.assertEqual(result['message'],
                         'maths and computer science already exists')
        assert response5.status_code == 400
        
    def test_get_courses(self):
        """Test that users can fetch all courses."""
        response = self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_admin_token())
        response1 = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/courses', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'], 'Courses successfull retrieved')
        assert response2.status_code == 200