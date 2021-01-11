import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime
from utils.serializer import Serializer


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
        self.curr.execute(
            ''' INSERT INTO checklist(student, department, course, certificate, year, campus, hostel, created_on)
            VALUES('{}','{}','{}','{}','{}','{}','{}','{}')
            RETURNING student, department, course, certificate, year, campus, hostel, created_on'''
            .format(self.admission_no, self.department_name, self.course_name, self.certificate_id, self.year_id, self.campus_id, self.hostel_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_forms(self):
        """Fetch all forms."""
        query = "SELECT * FROM checklist"
        response = Database().fetch(query)
        return response

    def get_form_by_id(self, checklist_id):
        """Get checklist form by id."""
        query = "SELECT * FROM checklist WHERE checklist_id=%s"
        response = Database().fetch_one(query, checklist_id)
        return response

    def get_form_by_admission_no(self, admission_no):
        """Get checklist form by id."""
        query = "SELECT * FROM checklist WHERE student=%s"
        response = Database().fetch_one(query, admission_no)
        return response

    def get_checklist_history_by_admission_no(self, admission_no):
        """Get checklist history by admission number."""
        query = "SELECT * FROM checklist WHERE student=%s"
        response = Database().fetch_group(query, admission_no)
        return response

    def update(self, checklist_id, department_name, course_name, certificate_id, year_id, campus_id, hostel_name):
        """Update checklist by id."""
        self.curr.execute(
            """UPDATE checklist SET department='{}', course='{}', certificate='{}', year='{}', campus='{}', hostel='{}' WHERE checklist_id={} RETURNING department, course, certificate, year, campus, hostel""".format(checklist_id, department_name, course_name, certificate_id, year_id, campus_id, hostel_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, checklist_id):
        """Delete checklist form by id."""
        self.curr.execute(
            """DELETE FROM checklist WHERE checklist_id={}""".format(checklist_id))
        self.conn.commit()
        self.curr.close()
