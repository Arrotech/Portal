import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ApplyCoursesModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, department_id=None, course_id=None, created_on=None):
        super().__init__()
        self.user_id = user_id
        self.department_id = department_id
        self.course_id = course_id
        self.created_on = datetime.now()

    def save(self):
        """Apply for a course."""
        try:
            self.curr.execute(
                ''' INSERT INTO apply_course(student, department, course, created_on)
                VALUES('{}','{}','{}','{}')
                RETURNING student, department, course, created_on'''
                .format(self.user_id, self.department_id, self.course_id, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"