import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, semester=None, year=None, admission_no=None, unit_name=None, marks=None, date=None):
        super().__init__()
        self.semester = semester
        self.year = year
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.marks = marks
        self.date = datetime.now()

    def save(self):
        """Create a new exam entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO exams(semester, year, student, unit, marks, date)
                VALUES('{}','{}','{}','{}','{}','{}')
                RETURNING semester, year, student, unit, marks, date'''
                .format(self.semester, self.year, self.admission_no, self.unit_name, self.marks, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_exams(self):
        """Fetch all exams."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname, us.lastname,
                          us.surname, e.marks, e.semester, e.year FROM exams AS e
                          INNER JOIN units AS un ON e.unit = un.unit_name
                          INNER JOIN users AS us ON e.student = us.admission_no
                          """)
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_exams_for_a_student_by_admission(self, admission_no):
        """A student can fetch all his examinations."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                          us.lastname, us.surname, e.marks FROM exams AS e
                          INNER JOIN units AS un ON e.unit = un.unit_name
                          INNER JOIN users AS us ON e.student = us.admission_no WHERE admission_no=%s
                          """, (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response
