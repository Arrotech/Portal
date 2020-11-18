import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ApplyCoursesModel(Database):
    """Initiallization."""

    def __init__(self, admission_no=None, institution_name=None, campus_id=None, certificate_id=None, department_name=None, course_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.institution_name = institution_name
        self.campus_id = campus_id
        self.certificate_id = certificate_id
        self.department_name = department_name
        self.course_name = course_name
        self.created_on = datetime.now()

    def save(self):
        """Apply for a course."""
        try:
            self.curr.execute(
                ''' INSERT INTO apply_course(student, institution, campus, certificate, department, course, created_on)
                VALUES('{}','{}','{}','{}','{}','{}','{}')
                RETURNING student, institution, campus, certificate, department, course, created_on'''
                .format(self.admission_no, self.institution_name, self.campus_id, self.certificate_id, self.department_name, self.course_name, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_course_by_id(self, application_id):
        """Get course by id."""
        query = "SELECT u.firstname, u.lastname, u.surname, u.admission_no, i.institution_name,\
                          d.department_name, c.course_name, ca.campus_name, ce.certificate_name\
                          FROM apply_course AS a\
                          INNER JOIN users AS u ON a.student=u.admission_no\
                          INNER JOIN institutions AS i on a.institution=i.institution_name\
                          INNER JOIN campuses AS ca ON a.campus=ca.campus_id\
                          INNER JOIN certificates AS ce ON a.certificate=ce.certificate_id\
                          INNER JOIN departments AS d ON a.department=d.department_name\
                          INNER JOIN courses AS c ON a.course=c.course_name\
                          WHERE application_id=%s"
        response = Database().fetch_one(query, application_id)
        return response
