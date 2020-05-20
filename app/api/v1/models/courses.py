import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class CoursesModel(Database):
    """Initiallization."""

    def __init__(self, course_name=None, department_id=None, created_on=None):
        super().__init__()
        self.course_name = course_name
        self.department_id = department_id
        self.created_on = datetime.now()

    def save(self):
        """Add a course."""
        self.curr.execute(
            ''' INSERT INTO courses(course_name, department, created_on)
            VALUES('{}','{}','{}')
            RETURNING course_name, department, created_on'''
            .format(self.course_name, self.department_id, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response


    def get_course_name(self, course_name):
        """Get course by name."""
        self.curr.execute("""
                          SELECT * FROM courses WHERE course_name='{}'
                          """.format(course_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def get_courses(self):
        """Get all courses."""
        self.curr.execute("""
                          SELECT departments.department_name, courses.course_name FROM courses
                          INNER JOIN departments ON courses.department = departments.department_id
                          """)
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def get_course_by_id(self, course_id):
        """Get course by id."""
        self.curr.execute("""
                          SELECT departments.department_name, courses.course_name FROM courses
                          INNER JOIN departments ON courses.department = departments.department_id
                          WHERE course_id={}
                          """.format(course_id))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response