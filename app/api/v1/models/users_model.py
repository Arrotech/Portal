import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None, admission_no=None, email=None, password=None, form=None, stream=None, role='student', date=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.admission_no = admission_no
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.form = form
        self.stream = stream
        self.role = role
        self.date = datetime.now()

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no, email, password, form, stream, role, date)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, email, password, form, stream, role, date'''
            .format(self.firstname, self.lastname, self.surname, self.admission_no, self.email, self.password,
                    self.form, self.stream, self.role, self.date))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_users(self):
        """Fetch all users"""
        query = "SELECT * from users"
        users = Database().fetch(query)
        return json.dumps(users, default=str)

    def get_user_id(self, user_id):
        """Request a single user with specific id."""
        self.curr.execute(
            """ SELECT * FROM users WHERE user_id={}""".format(user_id))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_admission_no(self, admission_no):
        """Request a single user with specific Admission Number."""
        self.curr.execute(
            """ SELECT * FROM users WHERE admission_no=%s""", (admission_no,))
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

    def promote_user(self, admission_no, form, stream):
        """Promote a student from one form to the next."""

        self.curr.execute("""UPDATE users SET form='{}', stream='{}' WHERE admission_no='{}' RETURNING admission_no, form, stream"""
                          .format(admission_no, form, stream))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def update_user_info(self, user_id, firstname, lastname, surname):
        """Update user information by id."""
        self.curr.execute(
            """UPDATE users SET firstname='{}', lastname='{}', surname='{}' WHERE user_id={} RETURNING firstname, lastname, surname""".format(user_id, firstname, lastname, surname))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def update_user_password(self, user_id, password):
        """Update user password by id."""
        self.curr.execute(
            """UPDATE users SET password='{}' WHERE user_id={} RETURNING password""".format(user_id, password))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(response, default=str)
