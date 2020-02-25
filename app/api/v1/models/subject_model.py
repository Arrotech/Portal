import json

from app.api.v1.models.database import Database

Database().create_table()


class SubjectsModel(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            form=None,
            stream=None,
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
        super().__init__()
        self.admission_no = admission_no
        self.form = form
        self.stream = stream
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
        """Create a new orders."""
        self.curr.execute(
            ''' INSERT INTO subjects(admission_no, form, stream, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business)\
            VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')\
            RETURNING admission_no, form, stream, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business''' \
                .format(self.admission_no, self.form, self.stream, self.maths, self.english, self.kiswahili, self.chemistry, self.biology, self.physics, self.history, self.geography, self.cre, self.agriculture,
                        self.business))
        subject = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(subject, default=str)

    def get_subjects(self):
        """Fetch all registered subjects."""
        self.curr.execute(''' SELECT * FROM subjects''')
        subjects = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(subjects, default=str)

    def get_admission_no(self, admission_no):
        """Get an exam with specific admission no."""
        self.curr.execute(""" SELECT * FROM subjects WHERE admission_no=%s""", (admission_no,))
        subject = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(subject, default=str)

    def edit_subjects(self, subject_id, admission_no, form, stream, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business):
        """Edit subjects."""

        self.curr.execute("""UPDATE subjects\
			SET admission_no='{}', form='{}', stream='{}', maths='{}', english='{}', kiswahili='{}', chemistry='{}', biology='{}', physics='{}', history='{}', geography='{}', cre='{}', agriculture='{}', business='{}'\
			WHERE subject_id={} RETURNING admission_no, form, stream, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business"""
            .format(subject_id, admission_no, form, stream, maths, english, kiswahili, chemistry, biology, physics, history, geography, cre, agriculture, business))
        subject = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(subject, default=str)