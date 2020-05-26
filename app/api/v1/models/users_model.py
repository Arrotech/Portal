import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None, admission_no=None, gender=None, email=None, password=None, current_year=None, role='student', is_confirmed=False, confirmed_on=None, created_on=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.admission_no = admission_no
        self.gender = gender
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.current_year = current_year
        self.role = role
        self.is_confirmed = is_confirmed
        self.confirmed_on = datetime.now()
        self.created_on = datetime.now()

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, current_year, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, gender, email, password, current_year, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname, self.admission_no, self.gender, self.email, self.password,
                    self.current_year, self.role, self.is_confirmed, self.created_on))
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

    def get_user_by_admission(self, admission_no):
        """Get user by admission."""
        self.curr.execute(
            """SELECT * FROM users WHERE admission_no=%s""", (admission_no,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(response, default=str)

    def get_admission_no(self, admission_no):
        """Request a single user with specific Admission Number."""
        self.curr.execute(
            """ SELECT u.firstname, u.lastname, u.surname, u.admission_no,
            u.gender, u.current_year, u.role, u.email, a.course FROM users AS u
            LEFT JOIN apply_course AS a ON u.admission_no=a.student
            WHERE admission_no=%s""", (admission_no,))
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

    def promote_user(self, admission_no, current_year):
        """Promote a student year to the next."""

        self.curr.execute("""UPDATE users SET current_year='{}' WHERE admission_no='{}' RETURNING admission_no, current_year"""
                          .format(admission_no, current_year))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def update_user_info(self, admission_no, firstname, lastname, surname):
        """Update user information by id."""
        self.curr.execute(
            """UPDATE users SET firstname='{}', lastname='{}', surname='{}' WHERE admission_no='{}' RETURNING firstname, lastname, surname""".format(admission_no, firstname, lastname, surname))
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

    def confirm_email(self, user_id, is_confirmed):
        """Confirm user email."""
        self.curr.execute(
            """UPDATE users SET is_confirmed=True WHERE user_id={} RETURNING is_confirmed, confirmed_on""".format(user_id, is_confirmed))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(response, default=str)
