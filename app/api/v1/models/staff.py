import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class StaffModel(Database):
    """Add a new user and retrieve User(s) by Id, Username or Email."""

    def __init__(self, firstname=None, lastname=None, form=None, stream=None, username=None, email=None, password=None, role='teacher', created_on=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.form = form
        self.stream = stream
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.role = role
        self.created_on = datetime.now()

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO staff(firstname, lastname, form, stream, username, email, password, role, created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, form, stream, username, email, password, role, created_on'''
            .format(self.firstname, self.lastname, self.form, self.stream, self.username, self.email, self.password, self.role,
                    self.created_on))
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
        query = "SELECT * FROM staff WHERE username=%s"
        response = Database().fetch_one(query, username)
        return json.dumps(response, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        query = "SELECT * FROM staff WHERE email=%s"
        response = Database().fetch_one(query, email)
        return json.dumps(response, default=str)

    def get_form(self, form):
        query = "SELECT * FROM staff WHERE form=%s"
        response = Database().fetch_one(query, form)
        return json.dumps(response, default=str)
