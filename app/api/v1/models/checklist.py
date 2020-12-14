import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ChecklistModel(Database):
    """Initiallization."""

    def __init__(self, admission_no=None, department_name=None, course_name=None, certificate_id=None, year_id=None, campus_id=None, hostel_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.department_name = department_name
        self.course_name = course_name
        self.certificate_id = certificate_id
        self.year_id = year_id
        self.campus_id = campus_id
        self.hostel_name = hostel_name
        self.created_on = datetime.now()

    def save(self):
        """Fill checklist form."""
        try:
            self.curr.execute(
                ''' INSERT INTO checklist(student, department, course, certificate, year, campus, hostel, created_on)
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING student, department, course, certificate, year, campus, hostel, created_on'''
                .format(self.admission_no, self.department_name, self.course_name, self.certificate_id, self.year_id, self.campus_id, self.hostel_name, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"