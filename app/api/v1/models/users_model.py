import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from utils.serializer import Serializer
from datetime import datetime


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None, admission_no=None, gender=None, email=None, password=None, role='student', is_confirmed=False, confirmed_on=None, created_on=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.admission_no = admission_no
        self.gender = gender
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.role = role
        self.is_confirmed = is_confirmed
        self.confirmed_on = datetime.now()
        self.created_on = datetime.now()

    def save_registrar(self, role='registrar'):
        """Save information of the new registrar."""
        try:
            self.curr.execute(
                ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed,  created_on)\
                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed, created_on'''
                .format(self.firstname, self.lastname, self.surname, self.admission_no, self.gender, self.email, self.password,
                        role, self.is_confirmed, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            Serializer.serialize(f"{e}", 500, "Error")

    def save_admin(self, role='admin'):
        """Save information of the new admin."""
        try:
            self.curr.execute(
                ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed,  created_on)\
                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed, created_on'''
                .format(self.firstname, self.lastname, self.surname, self.admission_no, self.gender, self.email, self.password,
                        role, self.is_confirmed, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            Serializer.serialize(f"{e}", 500, "Error")

    def save_accountant(self, role='accountant'):
        """Save information of the new accountant."""
        try:
            self.curr.execute(
                ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed,  created_on)\
                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed, created_on'''
                .format(self.firstname, self.lastname, self.surname, self.admission_no, self.gender, self.email, self.password,
                        role, self.is_confirmed, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            Serializer.serialize(f"{e}", 500, "Error")

    def save_student(self):
        """Save information of the new student."""
        try:
            self.curr.execute(
                ''' INSERT INTO users(firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed,  created_on)\
                    VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}') RETURNING firstname, lastname, surname, admission_no, gender, email, password, role, is_confirmed, created_on'''
                .format(self.firstname, self.lastname, self.surname, self.admission_no, self.gender, self.email, self.password,
                        self.role, self.is_confirmed, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")


    def get_all_users(self):
        """Fetch all users"""
        try:
            query = "SELECT * from users"
            response = Database().fetch(query)
            return response
        except Exception as e:
            Serializer.serialize(f"{e}", 500, "Error")

    def get_grouped_users(self, role):
        """Fetch all users by role."""
        try:
            query = "SELECT * FROM users WHERE role=%s"
            response = Database().fetch_group(query, role)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_user_by_id(self, user_id):
        """Request a single user with specific id."""
        try:
            query = "SELECT * FROM users WHERE user_id=%s"
            response = Database().fetch_one(query, user_id)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_user_by_admission(self, admission_no):
        """Get user by admission."""
        try:
            query = "SELECT * FROM users WHERE admission_no=%s"
            response = Database().fetch_one(query, admission_no)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_user_info(self, admission_no):
        """Request a single user with specific Admission Number."""
        try:
            query = "SELECT u.firstname, u.lastname, u.surname, u.admission_no,\
                u.gender, u.role, u.email, a.institution, a.campus, a.course, a.department, c.hostel, s.unit FROM users AS u\
                LEFT JOIN apply_course AS a ON u.admission_no=a.student\
                LEFT JOIN accommodation As c ON u.admission_no=c.student\
                LEFT JOIN subjects As s ON u.admission_no=s.student\
                WHERE admission_no=%s"
            response = Database().fetch_one(query, admission_no)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_user_by_email(self, email):
        """Request a single user with specific Email Address."""
        try:
            query = "SELECT * FROM users WHERE email=%s"
            response = Database().fetch_one(query, email)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def update_user_info(self, admission_no, firstname, lastname, surname, gender):
        """Update user information by admission number."""
        try:
            self.curr.execute(
                """UPDATE users SET firstname='{}', lastname='{}', surname='{}', gender='{}' WHERE admission_no='{}' RETURNING firstname, lastname, surname, gender""".format(admission_no, firstname, lastname, surname, gender))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def update_user_password(self, user_id, password):
        """Update user password by id."""
        try:
            self.curr.execute(
                """UPDATE users SET password='{}' WHERE user_id={} RETURNING password""".format(user_id, password))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def update_admin_role(self, user_id, role):
        """Update user role by id."""
        try:
            self.curr.execute(
                """UPDATE users SET role='{}' WHERE user_id={} RETURNING role""".format(user_id, role))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def confirm_user_email(self, user_id, is_confirmed):
        """Confirm user email."""
        try:
            self.curr.execute(
                """UPDATE users SET is_confirmed=True WHERE user_id={} RETURNING is_confirmed, confirmed_on""".format(user_id, is_confirmed))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")
