"""Json package."""
import json

from datetime import datetime

from app.api.v1.models.database import Database


class ExamsModel(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            term=None,
            form=None,
            exam_type=None,
            maths=None,
            english=None,
            kiswahili=None,
            chemistry=None,
            biology=None,
            physics=None,
            history=None,
            geography=None,
            cre=None,
            agriculture=None,
            business=None):
        """Initialization."""
        super().__init__()

        self.admission_no = admission_no
        self.term = term
        self.form = form
        self.exam_type = exam_type
        self.maths = maths
        self.english = english
        self.kiswahili = kiswahili
        self.chemistry = chemistry
        self.biology = biology
        self.physics = physics
        self.history = history
        self.geography = geography
        self.cre = cre
        self.agriculture = agriculture
        self.business = business

    def save(self):
        """Save new exam entry to the exams database."""
        self.curr.execute(
            ''' INSERT INTO exams(admission_no, term, form, exam_type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business)\
            VALUES('{}','{}','{}','{}',{},{},{},{},{},{},{},{},{},{},{})\
            RETURNING admission_no, term, form, exam_type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business'''
            .format(self.admission_no, self.term, self.form, self.exam_type, self.maths, self.english, self.kiswahili, self.chemistry, self.biology, self.physics, self.history, self.geography, self.cre,
                    self.agriculture, self.business))
        exam = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exam, default=str)

    def get_all_exams(self):
        """Fetch all exam entries for all students."""
        self.curr.execute(''' SELECT * FROM exams''')
        exams = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exams, default=str)

    def get_exams_by_admission_no(self, admission_no):
        """Fetch an exam by Admission Number."""
        self.curr.execute(
            """ SELECT * FROM exams WHERE admission_no='{}'""".format(admission_no))
        exams = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exams, default=str)

    def get_exam_by_admission_no(self, admission_no):
        """Fetch an exam by Admission Number."""
        self.curr.execute(
            """ SELECT * FROM exams WHERE admission_no='{}'""".format(admission_no))
        exam = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exam, default=str)

    def get_exams_by_form_and_term(self, form, term):
        """Fetch exams by form"""
        self.curr.execute(
            """ SELECT * FROM exams WHERE form='{}' and term='{}'""".format(form, term))
        exams = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exams, default=str)

    def delete_exam(self, admission_no):
        ''' Delete an exam by Admission Number.'''
        self.curr.execute(
            """ DELETE FROM exams WHERE admission_no='{}'""", (admission_no,))
        self.conn.commit()
        self.curr.close()

    def edit_exams(self, exam_id, admission_no, term, form, exam_type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business):
        """User can Change exams marks."""

        self.curr.execute("""UPDATE exams\
			SET admission_no='{}', term='{}', form='{}', exam_type='{}', maths='{}', english='{}', kiswahili='{}', chemistry='{}', biology='{}', physics='{}', history='{}', geography='{}', cre='{}', agriculture='{}', business='{}'\
			WHERE exam_id={} RETURNING admission_no, term, form, exam_type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business"""
            .format(exam_id, admission_no, term, form, exam_type, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business))
        exam = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(exam, default=str)
