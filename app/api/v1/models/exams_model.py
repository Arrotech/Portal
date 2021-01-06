import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime
from utils.serializer import Serializer


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, year_id=None, admission_no=None, unit_name=None, marks=None, exam_type=None, created_on=None):
        super().__init__()
        self.year_id = year_id
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.marks = marks
        self.exam_type = exam_type
        self.created_on = datetime.now()

    def save(self):
        """Create a new exam entry."""
        self.curr.execute(
            ''' INSERT INTO exams(year, student, unit, marks, exam_type, created_on)
            VALUES('{}','{}','{}','{}','{}','{}')
            RETURNING year, student, unit, marks, exam_type, created_on'''
            .format(self.year_id, self.admission_no, self.unit_name, self.marks, self.exam_type, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_exams_for_specific_student(self, admission_no):
        """A student can fetch all his examinations."""
        self.curr.execute("""SELECT un.unit_code, a.year, a.semester, e.marks, e.exam_type FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name WHERE admission_no=%s
                        """, (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_exams_for_specific_year(self, admission_no, year):
        """A student can fetch all his examinations for the specified year."""
        self.curr.execute("""SELECT un.unit_code, a.year, a.semester, e.marks, e.exam_type FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name WHERE admission_no=%s AND a.year=%s""", (admission_no, year,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_exams_for_specific_semester(self, admission_no, year, semester):
        """A student can fetch all his examinations for the specified semester."""
        self.curr.execute("""SELECT un.unit_code, a.year, a.semester, e.marks, e.exam_type FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name WHERE admission_no=%s AND a.year=%s AND a.semester=%s""", (admission_no, year, semester))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

        # exam_id   year_id   admission_no     unit_name   marks   exam_type   created_on
        # 1         1         sc200-1358-2014  calculus    62      MAIN        wigfgwFGIGF

        # exam_id   year_id   admission_no     unit_name   marks   exam_type   created_on
        # 2         1         sc200-1358-2014  calculus    28      CAT        wigfgwFGIGF

        # ------- Query for the summation of Main and CAT for a particular unit ----------

        # year_id   admission_no     unit_name   marks
        # 1         sc200-1358-2014  calculus    90

        # ------- Query for the summation of several units for a particular year and semester ---------

        # year_id   admission_no     unit_name   marks
        # 1         sc200-1358-2014  calculus    90

    def fetch_total_for_specific_unit(self, admission_no, unit):
        """A student can fetch all his examinations for the specified semester."""
        self.curr.execute("""SELECT a.year, a.semester, unit, SUM(marks) as total FROM exams as e
         INNER JOIN academic_year AS a ON e.year = a.year_id
         WHERE student=%s AND unit=%s GROUP BY a.year, a.semester, unit""", (admission_no, unit,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response
