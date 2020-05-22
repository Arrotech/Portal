import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, semester=None, year=None, user_id=None, unit_id=None, marks=None, date=None):
        super().__init__()
        self.semester = semester
        self.year = year
        self.user_id = user_id
        self.unit_id = unit_id
        self.marks = marks
        self.date = datetime.now()

    def save(self):
        """Create a new exam entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO exams(semester, year, student, unit, marks, date)
                VALUES('{}','{}','{}','{}','{}','{}')
                RETURNING semester, year, student, unit, marks, date'''
                .format(self.semester, self.year, self.user_id, self.unit_id, self.marks, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_exams(self):
        """Fetch all exams."""
        self.curr.execute("""
                          SELECT units.unit_name, units.unit_code, users.admission_no, marks, semester, year FROM exams
                          INNER JOIN units ON exams.unit = units.unit_id
                          INNER JOIN users ON exams.student = users.user_id
                          """)
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_exams_for_a_student(self, year, user_id):
        """A student can fetch all his examinations for a specific year."""
        self.curr.execute("""
                          SELECT units.unit_name, units.unit_code, users.admission_no, marks FROM exams
                          INNER JOIN units ON exams.unit = units.unit_id
                          INNER JOIN users ON exams.student = users.user_id WHERE year='{}' and user_id={}
                          """.format(year, user_id))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response
