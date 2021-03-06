from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None,
                 admission_no=None, gender=None, email=None, password=None,
                 role='student', is_confirmed=False, confirmed_on=None,
                 created_on=None):
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
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_college_head(self, role='college'):
        """Save information of the new college head."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_department_head(self, role='department'):
        """Save information of the new department head."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_admin(self, role='admin'):
        """Save information of the new admin."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_librarian(self, role='librarian'):
        """Save information of the new admin."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_accountant(self, role='accountant'):
        """Save information of the new accountant."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_hostel_manager(self, role='hostel'):
        """Save information of the new accountant."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def save_student(self):
        """Save information of the new student."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, admission_no,\
                    gender, email, password, role, is_confirmed,  created_on)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                RETURNING firstname, lastname, surname, admission_no, gender,\
                    email, password, role, is_confirmed, created_on'''
            .format(self.firstname, self.lastname, self.surname,
                    self.admission_no, self.gender, self.email, self.password,
                    self.role, self.is_confirmed, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_users(self):
        """Fetch all users"""
        query = "SELECT * from users"
        response = Database().fetch(query)
        return response

    def get_grouped_users(self, role):
        """Fetch all users by role."""
        query = "SELECT * FROM users WHERE role=%s"
        response = Database().fetch_group(query, role)
        return response

    def number_of_users(self, role):
        """Fetch the total number of specific users."""
        query = "SELECT COUNT(*) FROM users WHERE role=%s"
        response = Database().fetch_one(query, role)
        return response

    def get_user_by_id(self, user_id):
        """Request a single user with specific id."""
        query = "SELECT * FROM users WHERE user_id=%s"
        response = Database().fetch_one(query, user_id)
        return response

    def get_user_by_admission(self, admission_no):
        """Get user by admission."""
        query = "SELECT * FROM users WHERE admission_no=%s"
        response = Database().fetch_one(query, admission_no)
        return response

    def get_user_info(self, admission_no):
        """Request a single user with specific Admission Number."""
        query = "SELECT u.firstname, u.lastname, u.surname, u.admission_no,\
            u.gender, u.role, u.email, a.institution, cmp.campus_name, a.course,\
                a.department, c.hostel, s.unit FROM users AS u\
            LEFT JOIN apply_course AS a ON u.admission_no=a.student\
            LEFT JOIN accommodation As c ON u.admission_no=c.student\
            LEFT JOIN subjects As s ON u.admission_no=s.student\
            LEFT JOIN campuses AS cmp ON a.campus=cmp.campus_id\
            WHERE admission_no=%s"
        response = Database().fetch_one(query, admission_no)
        return response

    def get_user_by_email(self, email):
        """Request a single user with specific Email Address."""
        query = "SELECT * FROM users WHERE email=%s"
        response = Database().fetch_one(query, email)
        return response

    def update_user_info(self, admission_no, firstname, lastname, surname,
                         gender):
        """Update user information by admission number."""
        self.curr.execute(
            """UPDATE users SET firstname='{}', lastname='{}', surname='{}',\
                gender='{}' WHERE admission_no='{}' RETURNING firstname,\
                    lastname, surname, gender"""
            .format(admission_no, firstname, lastname, surname, gender))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def update_user_password(self, user_id, password):
        """Update user password by id."""
        self.curr.execute(
            """UPDATE users SET password='{}' WHERE user_id={}
            RETURNING password""".format(user_id, password))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def update_admin_role(self, user_id, role):
        """Update user role by id."""
        self.curr.execute(
            """UPDATE users SET role='{}' WHERE user_id={} RETURNING role"""
            .format(user_id, role))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def confirm_user_email(self, user_id, is_confirmed):
        """Confirm user email."""
        self.curr.execute(
            """UPDATE users SET is_confirmed=True WHERE user_id={}
            RETURNING is_confirmed""".format(user_id, is_confirmed))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
