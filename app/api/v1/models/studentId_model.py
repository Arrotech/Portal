import json

from app.api.v1.models.database import Database


class StudentIdModel(Database):
    """Initialization."""

    def __init__(self, surname=None, first_name=None, last_name=None, admission_no=None):
        super().__init__()
        self.surname = surname
        self.first_name = first_name
        self.last_name = last_name
        self.admission_no = admission_no

    def save(self):
        """Save information of the new user"""

        self.curr.execute(
            ''' INSERT INTO studentId(surname, first_name, last_name, admission_no)\
             VALUES('{}','{}','{}','{}') RETURNING surname, first_name, last_name, admission_no''' \
                .format(self.surname, self.first_name, self.last_name, self.admission_no))
        studentId = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(studentId, default=str)

    def get_all(self):
        """Fetch all users"""

        self.curr.execute(''' SELECT * FROM studentId''')
        studentId = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(studentId, default=str)

    def get_admission_no(self, admission_no):
        """Get an exam with specific admission no."""
        self.curr.execute(""" SELECT * FROM studentId WHERE admission_no=%s""", (admission_no,))
        studentId = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(studentId, default=str)
