import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class StaffModel(Database):
    """Add a new user and retrieve User(s) by Id, Username or Email."""

    def __init__(self, firstname=None, lastname=None, form=None, username=None, email=None, password=None, role='teacher', date=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.form = form
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.role = role
        self.date = datetime.now()

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO staff(firstname, lastname, form, username, email, password, role, date)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, form, username, email, password, role, date'''
            .format(self.firstname, self.lastname, self.form, self.username, self.email, self.password, self.role,
                    self.date))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_users(self):
        "Get all users."
        query = "SELECT * from staff"
        users = Database().fetch(query)
        return json.dumps(users, default=str)

    def get_username(self, username):
        """Request a single user with specific Username."""
        self.curr.execute(
            """ SELECT * FROM staff WHERE username=%s""", (username,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        self.curr.execute(''' SELECT * FROM staff WHERE email=%s''', (email,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_form(self, form):
        """Request a single user with specific form."""
        self.curr.execute(''' SELECT * FROM staff WHERE form=%s''', (form,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)