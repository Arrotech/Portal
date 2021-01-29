from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect
from app import db


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True)
    firstname = db.Column(db.String(50), unique=False, nullable=False)
    lastname = db.Column(db.String(50), unique=False)
    surname = db.Column(db.String(50), unique=False)
    admission_no = db.Column(db.String(50), primary_key=True, unique=True,
                             nullable=False)
    gender = db.Column(db.String(50), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50), unique=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, default=datetime.utcnow)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship('ApplyCourse', backref='student_obj',
                              cascade="all, delete", passive_deletes=True)

    def __init__(self, firstname=None, lastname=None, surname=None,
                 admission_no=None, gender=None, username=None, email=None,
                 password=None, role='student', is_confirmed=False,
                 confirmed_on=None, created_on=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.admission_no = admission_no
        self.gender = gender
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.role = role
        self.is_confirmed = is_confirmed
        self.confirmed_on = datetime.now()
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<User '{}'>".format(self.firstname)
