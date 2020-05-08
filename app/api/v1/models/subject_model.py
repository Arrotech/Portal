import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class SubjectsModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, unit_id=None, date=None):
        super().__init__()
        self.user_id = user_id
        self.unit_id = unit_id
        self.date = datetime.now()

    def save(self):
        """Create a new orders."""
        try:
            self.curr.execute(
                ''' INSERT INTO subjects(student, unit, date)
                VALUES('{}','{}','{}')
                RETURNING student, unit, date'''
                .format(self.user_id, self.unit_id, self.date))
            subject = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return subject
        except psycopg2.IntegrityError:
            return "error"

    def get_subjects(self):
        """Fetch all subjects."""
        self.curr.execute("""
                          SELECT units.unit_name, units.unit_code, users.admission_no FROM subjects
                          INNER JOIN units ON subjects.unit = units.unit_id
                          INNER JOIN users ON subjects.student = users.user_id
                          """)
        subjects = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return subjects
    
    def get_subject_by_id(self, subject_id):
        """Fetch a subject by id."""
        self.curr.execute("""SELECT * FROM subjects WHERE subject_id={}""".format(subject_id))
        subject = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return subject
    
    def get_subjects_for_specific_user_by_id(self, user_id):
        """Fetch all subjects by a single user."""
        self.curr.execute("""
                          SELECT units.unit_name, units.unit_code, users.admission_no FROM subjects
                          INNER JOIN units ON subjects.unit = units.unit_id
                          INNER JOIN users ON subjects.student = users.user_id WHERE user_id={}
                          """.format(user_id))
        subjects = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return subjects
    
    def delete(self, subject_id):
        """Delete a subject by id."""
        self.curr.execute(
            """DELETE FROM subjects WHERE subject_id={}""".format(subject_id))
        self.conn.commit()
        self.curr.close()
