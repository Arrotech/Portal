import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database


class TeachersModel(Database):
    """Add a new user and retrieve User(s) by Id or Email."""

    def __init__(self, firstname=None, lastname=None, email=None, password=None, form=None, role='admin'):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.form = form
        self.role = role

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO teachers(firstname, lastname, email, password, form, role)\
                VALUES('{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, email, password, form, role''' \
                .format(self.firstname, self.lastname, self.email, self.password, self.form, self.role))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_teachers(self):
        """Request for all users."""
        self.curr.execute(''' SELECT * FROM teachers''')
        users = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(users, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        self.curr.execute(''' SELECT * FROM teachers WHERE email=%s''', (email,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)
