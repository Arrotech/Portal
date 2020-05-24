import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class CoursesModel(Database):
    """Initiallization."""

    def __init__(self, course_name=None, department_name=None, created_on=None):
        super().__init__()
        self.course_name = course_name
        self.department_name = department_name
        self.created_on = datetime.now()

    def save(self):
        """Add a course."""
        self.curr.execute(
            ''' INSERT INTO courses(course_name, department, created_on)
            VALUES('{}','{}','{}')
            RETURNING course_name, department, created_on'''
            .format(self.course_name, self.department_name, self.created_on))
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
        self.curr.execute("""SELECT d.department_name, c.course_name 
                          FROM courses AS c
                          INNER JOIN departments AS d ON c.department = d.department_name
                          """)
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_course_by_id(self, course_id):
        """Get course by id."""
        self.curr.execute("""SELECT d.department_name, c.course_name 
                          FROM courses AS c
                          INNER JOIN departments AS d ON c.department = d.department_name
                          WHERE course_id={}
                          """.format(course_id))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_course(self, course_id, course_name, department_name):
        """Update course."""
        self.curr.execute(
            """UPDATE courses SET course_name='{}', department='{}' WHERE course_id={} RETURNING course_name, department""".format(course_id, course_name, department_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, course_id):
        """Delete course by id."""
        self.curr.execute(
            """DELETE FROM courses WHERE course_id={}""".format(course_id))
        self.conn.commit()
        self.curr.close()
