import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class SubjectsModel(Database):
    """Initiallization."""

    def __init__(self, admission_no=None, unit_name=None, date=None):
        super().__init__()
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.date = datetime.now()

    def save(self):
        """Register a subject."""
        try:
            self.curr.execute(
                ''' INSERT INTO subjects(student, unit, date)
                VALUES('{}','{}','{}')
                RETURNING student, unit, date'''
                .format(self.admission_no, self.unit_name, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_subjects(self):
        """Fetch all subjects."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                          us.lastname, us.surname 
                          FROM subjects AS s
                          INNER JOIN units AS un ON s.unit = un.unit_name
                          INNER JOIN users AS us ON s.student = us.admission_no
                          """)
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_subject_by_id(self, subject_id):
        """Fetch a subject by id."""
        self.curr.execute(
            """SELECT * FROM subjects WHERE subject_id={}""".format(subject_id))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_subjects_for_specific_user_by_admission(self, admission_no):
        """Fetch all subjects for a single user."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                          us.lastname, us.surname
                          FROM subjects AS s
                          INNER JOIN units AS un ON s.unit = un.unit_name
                          INNER JOIN users AS us ON s.student = us.admission_no
                          WHERE admission_no=%s
                          """, (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, subject_id):
        """Delete a subject by id."""
        self.curr.execute(
            """DELETE FROM subjects WHERE subject_id={}""".format(subject_id))
        self.conn.commit()
        self.curr.close()
