import json
from app.api.v1.models.database import Database
from datetime import datetime


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, year_id=None, admission_no=None, unit_name=None,
                 marks=None, exam_type=None, created_on=None):
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
            .format(self.year_id, self.admission_no, self.unit_name,
                    self.marks, self.exam_type, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_exams_for_specific_student(self, admission_no):
        """A student can fetch all his examinations."""
        self.curr.execute("""SELECT un.unit_code, a.year, a.semester, e.marks\
                            FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE admission_no=%s
                        """, (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_exam_by_id(self, exam_id):
        """Fetch an exam by id."""
        query = "SELECT * FROM exams WHERE exam_id=%s"
        response = Database().fetch_one(query, exam_id)
        return response

    def fetch_all_exams_for_specific_year(self, admission_no, year):
        """A student can fetch all his examinations for the specified year."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, a.year,\
                            a.semester, e.marks FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE admission_no=%s AND a.year=%s""", (admission_no,
                                                                 year,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_exams_for_specific_semester(self, admission_no, year,
                                              semester):
        """A student can fetch all examinations for the specified semester."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, a.year,\
                            a.semester, e.marks FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE admission_no=%s AND a.year=%s AND\
                            a.semester=%s""", (admission_no, year, semester))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_aggregated_points(self, admission_no):
        """A student can view their aggregated points."""
        self.curr.execute("""SELECT AVG(CAST(e.marks AS FLOAT)) AS aggregate
                        FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE student=%s""",
                          (admission_no,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_aggregated_points(self, admission_no, year):
        """A student can view their aggregated points for a specific year."""
        self.curr.execute("""SELECT a.year, AVG(CAST(e.marks AS FLOAT)) AS aggregate
                        FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE student=%s AND a.year=%s GROUP BY a.year""",
                          (admission_no,
                           year,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_all_supplementaries(self, admission_no):
        """Fetch all supplementaries for a student."""
        self.curr.execute("""SELECT COUNT(*)
                        FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE admission_no=%s AND e.marks<50""",
                          (admission_no,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_supplementaries(self, admission_no, year):
        """Fetch supplementaries for an year."""
        self.curr.execute("""SELECT COUNT(*)
                        FROM exams AS e
                        INNER JOIN academic_year AS a ON e.year = a.year_id
                        INNER JOIN users AS us ON e.student = us.admission_no
                        INNER JOIN units AS un ON e.unit = un.unit_name\
                        WHERE admission_no=%s AND a.year=%s AND e.marks<50""",
                          (admission_no,
                           year,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def fetch_total_for_specific_unit(self, admission_no, unit):
        """A student can fetch all examinations for the specified semester."""
        self.curr.execute("""SELECT a.year, a.semester, unit, SUM(marks) as total FROM exams as e
         INNER JOIN academic_year AS a ON e.year = a.year_id
         WHERE student=%s AND unit=%s GROUP BY a.year, a.semester, unit""", (
            admission_no, unit,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def update(self, exam_id, year, student, unit, marks, exam_type):
        """Update exam entry."""
        self.curr.execute(
            """UPDATE exams SET year='{}', student='{}', unit='{}', marks='{}',\
            exam_type='{}' WHERE exam_id={} RETURNING year, student, unit,\
            marks, exam_type"""
            .format(exam_id, year, student, unit, marks, exam_type))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, exam_id):
        """Delete exam by id."""
        self.curr.execute(
            """DELETE FROM exams WHERE exam_id={}""".format(exam_id))
        self.conn.commit()
        self.curr.close()
