import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None, admission_no=None, email=None, password=None, form=None, role='student'):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.admission_no = admission_no
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.form = form
        self.role = role

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no, email, password, form, role)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, email, password, form, role''' \
                .format(self.firstname, self.lastname, self.surname, self.admission_no, self.email, self.password,
                        self.form, self.role))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_users(self):
        """Request for all users."""
        self.curr.execute(''' SELECT * FROM users''')
        users = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(users, default=str)

    def get_admission_no(self, admission_no):
        """Request a single user with specific Admission Number."""
        self.curr.execute(""" SELECT * FROM users WHERE admission_no=%s""", (admission_no,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        self.curr.execute(''' SELECT * FROM users WHERE email=%s''', (email,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)
