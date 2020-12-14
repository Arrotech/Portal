import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime
from utils.serializer import Serializer


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, year_id=None, admission_no=None, unit_name=None, marks=None, created_on=None):
        super().__init__()
        self.year_id = year_id
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.marks = marks
        self.created_on = datetime.now()

    def save(self):
        """Create a new exam entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO exams(year, student, unit, marks, created_on)
                VALUES('{}','{}','{}','{}','{}')
                RETURNING year, student, unit, marks, created_on'''
                .format(self.year_id, self.admission_no, self.unit_name, self.marks, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def fetch_all_exams_for_specific_student(self, admission_no):
        """A student can fetch all his examinations."""
        try:
            self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                            us.lastname, us.surname, a.year, a.semester, e.marks FROM exams AS e
                            INNER JOIN academic_year AS a ON e.year = a.year_id
                            INNER JOIN users AS us ON e.student = us.admission_no
                            INNER JOIN units AS un ON e.unit = un.unit_name WHERE admission_no=%s
                            """, (admission_no,))
            response = self.curr.fetchall()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def fetch_all_exams_for_specific_year(self, admission_no, year):
        """A student can fetch all his examinations for the specified year."""
        try:
            self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                            us.lastname, us.surname, a.year, a.semester, e.marks FROM exams AS e
                            INNER JOIN academic_year AS a ON e.year = a.year_id
                            INNER JOIN users AS us ON e.student = us.admission_no
                            INNER JOIN units AS un ON e.unit = un.unit_name WHERE admission_no=%s AND a.year=%s""", (admission_no, year,))
            response = self.curr.fetchall()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")
