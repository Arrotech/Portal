import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class SubjectsModel(Database):
    """Initiallization."""

    def __init__(self, admission_no=None, unit_name=None, year_id=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.year_id = year_id
        self.created_on = datetime.now()

    def save(self):
        """Register a subject."""
        self.curr.execute(
            ''' INSERT INTO subjects(student, unit, year, created_on)
            VALUES('{}','{}','{}','{}')
            RETURNING student, unit, year, created_on'''
            .format(self.admission_no, self.unit_name, self.year_id, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_subjects(self):
        """Fetch all subjects."""
        query = "SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,\
                          us.lastname, us.surname FROM subjects AS s\
                          INNER JOIN units AS un ON s.unit = un.unit_name\
                          INNER JOIN users AS us ON s.student = us.admission_no"
        response = Database().fetch(query)
        return response

    def get_subject_by_id(self, subject_id):
        """Fetch a subject by id."""
        query = "SELECT * FROM subjects WHERE subject_id=%s"
        response = Database().fetch_one(query, subject_id)
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

    def get_subjects_for_specific_user_by_year(self, admission_no, year):
        """Fetch all subjects for a single user for a specific year."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                          us.lastname, us.surname, a.year, a.semester
                          FROM subjects AS s
                          INNER JOIN units AS un ON s.unit = un.unit_name
                          INNER JOIN users AS us ON s.student = us.admission_no
                          INNER JOIN academic_year AS a ON s.year = a.year_id
                          WHERE admission_no=%s AND a.year=%s
                          """, (admission_no, year,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_subjects_for_specific_user_by_semester(self, admission_no, year, semester):
        """Fetch all subjects for a single user for a specific semester."""
        self.curr.execute("""SELECT un.unit_name, un.unit_code, us.admission_no, us.firstname,
                          us.lastname, us.surname, a.year, a.semester
                          FROM subjects AS s
                          INNER JOIN units AS un ON s.unit = un.unit_name
                          INNER JOIN users AS us ON s.student = us.admission_no
                          INNER JOIN academic_year AS a ON s.year = a.year_id
                          WHERE admission_no=%s AND a.year=%s AND a.semester=%s 
                          """, (admission_no, year, semester,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_subject_by_id(self, subject_id, unit_name):
        """Update subject by id."""
        self.curr.execute(
            """UPDATE subjects SET unit='{}' WHERE subject_id={} RETURNING unit""".format(subject_id, unit_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, subject_id):
        """Delete a subject by id."""
        self.curr.execute(
            """DELETE FROM subjects WHERE subject_id={}""".format(subject_id))
        self.conn.commit()
        self.curr.close()
