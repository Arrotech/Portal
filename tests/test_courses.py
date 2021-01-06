import json

from utils.v1.dummy.courses import new_course, add_course_keys, add_non_exisitng_department,\
    course_name_exists, update_course, update_course_name_exists, update_course_keys
from utils.v1.dummy.departments import new_department
from .base_test import BaseTest


class TestCourses(BaseTest):
    """Test courses."""

    def test_add_course(self):
        """Test that admin can add a course."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        response = self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(
            result['message'], 'maths and computer science added successfully')
        assert response.status_code == 201

    def test_add_course_keys(self):
        """Test that an admin cannot add a course with an invalid key."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        response = self.client.post(
            '/api/v1/courses', data=json.dumps(add_course_keys), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid course_name key')
        assert response.status_code == 400

    def test_add_course_for_non_existing_department(self):
        """Test that an admin cannot add a course for non existing department."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/courses', data=json.dumps(add_non_exisitng_department), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Department not found')
        assert response.status_code == 404

    def test_add_course_for_already_existing_course_name(self):
        """Test that an admin cannot add a course for non existing department."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.post(
            '/api/v1/courses', data=json.dumps(course_name_exists), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'maths and computer science already exists')
        assert response.status_code == 400

    def test_get_courses(self):
        """Test that users can fetch all courses."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/courses', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Courses successfull retrieved')
        assert response.status_code == 200

    def test_get_course(self):
        """Test that users can fetch course by id."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/courses/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course successfull retrieved')
        assert response.status_code == 200

    def test_get_course_non_existing_course(self):
        """Test that users cannot fetch non existing course by id."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/courses/100', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course not found')
        assert response.status_code == 404

    def test_edit_course_by_id(self):
        """Test that an admin can edit course by id."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/courses/1', data=json.dumps(update_course), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course updated successfully')
        assert response.status_code == 200

    def test_edit_course_by_id_keys(self):
        """Test that an admin cannot edit course by id with an invalid json key."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/courses/1', data=json.dumps(update_course_keys), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid course_name key')
        assert response.status_code == 400

    def test_edit_existing_course_name(self):
        """Test that an admin cannot edit course with already existing course name."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/courses/1', data=json.dumps(update_course_name_exists), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'maths and computer science already exists')
        assert response.status_code == 400

    def test_edit_non_existing_course(self):
        """Test that an admin cannot edit non existing course."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.put(
            '/api/v1/courses/100', data=json.dumps(update_course), content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course not found')
        assert response.status_code == 404

    def test_delete_course_by_id(self):
        """Test that an admin can delete course by id."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.delete(
            '/api/v1/courses/1', content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_course(self):
        """Test that an admin cannot delete non existing course."""
        self.client.post(
            '/api/v1/departments', data=json.dumps(new_department), content_type='application/json',
            headers=self.get_college_head_token())
        self.client.post(
            '/api/v1/courses', data=json.dumps(new_course), content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.delete(
            '/api/v1/courses/100', content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Course not found')
        assert response.status_code == 404
