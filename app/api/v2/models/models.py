from datetime import datetime
from werkzeug.security import generate_password_hash
from sqlalchemy import inspect
from app.__init__ import db


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

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<User '{}'>".format(self.firstname)


class Institution(db.Model):
    """ Institution Model for storing institution related details """
    __tablename__ = "institutions"

    institution_id = db.Column(
        db.Integer, autoincrement=True)
    institution_name = db.Column(
        db.String(120), primary_key=True, unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship(
        'ApplyCourse', backref='institution_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, institution_name=None, created_on=None):
        super().__init__()
        self.institution_name = institution_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Institution '{}'>".format(self.institution_name)


class Campus(db.Model):
    """ Campus Model for storing campus related details """
    __tablename__ = "campuses"

    campus_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    campus_name = db.Column(db.String(120), unique=False, nullable=False)
    campus_location = db.Column(db.String(120), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship(
        'ApplyCourse', backref='campus_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, campus_name=None, campus_location=None,
                 created_on=None):
        super().__init__()
        self.campus_name = campus_name
        self.campus_location = campus_location
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Campus '{}'>".format(self.campus_name)


class Certificate(db.Model):
    """ Certificate Model for storing certificate related details """
    __tablename__ = "certificates"

    certificate_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    certificate_name = db.Column(db.String(120), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship(
        'ApplyCourse', backref='certificate_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, certificate_name=None, created_on=None):
        super().__init__()
        self.certificate_name = certificate_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Certificate '{}'>".format(self.certificate_name)


class Department(db.Model):
    """ Department Model for storing department related details """
    __tablename__ = "departments"

    department_id = db.Column(
        db.Integer, autoincrement=True)
    department_name = db.Column(
        db.String(120), primary_key=True, unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship(
        'Course', backref='department_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, department_name=None, created_on=None):
        super().__init__()
        self.department_name = department_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Department '{}'>".format(self.department_name)


class Unit(db.Model):
    """ Unit Model for storing unit related details """
    __tablename__ = "units"

    unit_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    unit_name = db.Column(db.String(120), unique=True, nullable=False)
    unit_code = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    units = db.relationship('UnitRegistration', backref='unit_obj',
                            cascade="all, delete", passive_deletes=True)

    def __init__(self, unit_name=None, unit_code=None, created_on=None):
        super().__init__()
        self.unit_name = unit_name
        self.unit_code = unit_code
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Unit '{}'>".format(self.unit_name)


class Year(db.Model):
    """ Year Model for storing year related details """
    __tablename__ = "academic_year"

    year_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.String(120), unique=False, nullable=False)
    semester = db.Column(db.String(50), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    units = db.relationship('UnitRegistration', backref='year_obj',
                            cascade="all, delete", passive_deletes=True)

    def __init__(self, year=None, semester=None, created_on=None):
        super().__init__()
        self.year = year
        self.semester = semester
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Year '{}'>".format(self.year)


class Hostel(db.Model):
    """ Hostel Model for storing hostel related details """
    __tablename__ = "hostels"

    hostel_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    hostel_name = db.Column(db.String(120), unique=True, nullable=False)
    rooms = db.Column(db.Integer, unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    hostel_location = db.Column(db.String(120), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    hostels = db.relationship(
        'Accommodation', backref='hostel_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, hostel_name=None, rooms=None, gender=None,
                 hostel_location=None, created_on=None):
        super().__init__()
        self.hostel_name = hostel_name
        self.rooms = rooms
        self.gender = gender
        self.hostel_location = hostel_location
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Hostel '{}'>".format(self.hostel_name)


class Course(db.Model):
    """ Course Model for storing course related details """
    __tablename__ = "courses"

    course_id = db.Column(
        db.Integer, autoincrement=True)
    course_name = db.Column(
        db.String(120), primary_key=True, unique=True, nullable=False)
    department = db.Column(db.String(120), db.ForeignKey(
        'departments.department_name', ondelete='CASCADE'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    courses = db.relationship(
        'ApplyCourse', backref='course_obj', cascade="all, delete",
        passive_deletes=True)

    def __init__(self, course_name=None, department_name=None,
                 created_on=None):
        super().__init__()
        self.course_name = course_name
        self.department_name = department_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Course '{}'>".format(self.course_name)


class ApplyCourse(db.Model):
    """ ApplyCourse Model for storing course application related details """
    __tablename__ = "apply_course"

    application_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    institution = db.Column(db.String(120), db.ForeignKey(
        'institutions.institution_name', ondelete='CASCADE'), nullable=False)
    campus = db.Column(db.Integer, db.ForeignKey(
        'campuses.campus_id', ondelete='CASCADE'), nullable=False)
    certificate = db.Column(db.Integer, db.ForeignKey(
        'certificates.certificate_id', ondelete='CASCADE'), nullable=False)
    department = db.Column(db.String(120), db.ForeignKey(
        'departments.department_name', ondelete='CASCADE'), nullable=False)
    course = db.Column(db.String(120), db.ForeignKey(
        'courses.courses_name', ondelete='CASCADE'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, admission_no=None, institution_name=None,
                 campus_id=None, certificate_id=None, department_name=None,
                 course_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.institution_name = institution_name
        self.campus_id = campus_id
        self.certificate_id = certificate_id
        self.department_name = department_name
        self.course_name = course_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return "<Course '{}'>".format(self.course_name)

# start db.relationship from here


class UnitRegistration(db.Model):
    """ Unit registration Model for storing unit related details """
    __tablename__ = "subjects"

    exam_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    unit = db.Column(db.String(120), db.ForeignKey(
        'units.unit_name', ondelete='CASCADE'), nullable=False)
    year = db.Column(db.Integer, db.ForeignKey(
        'academic_year.year_id', ondelete='CASCADE'), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, admission_no=None, unit_name=None, year_id=None,
                 created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.year_id = year_id
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"UnitRegistration('{self.unit_name}', '{self.admission_no}')"


class Exam(db.Model):
    """ Exam Model for storing exam related details """
    __tablename__ = "exams"

    exam_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer, db.ForeignKey(
        'academic_year.year_id', ondelete='CASCADE'), nullable=False)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    unit = db.Column(db.String(120), db.ForeignKey(
        'units.unit_name', ondelete='CASCADE'), nullable=False)
    marks = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, year_id=None, admission_no=None, unit_name=None,
                 marks=None, exam_type=None, created_on=None):
        super().__init__()
        self.year_id = year_id
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.marks = marks
        self.exam_type = exam_type
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Exam('{self.unit_name}', '{self.marks}')"


class Fee(db.Model):
    """ Fee Model for storing fee related details """
    __tablename__ = "fees"

    fee_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(), unique=False, nullable=False)
    transaction_no = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(
            self,
            admission_no=None,
            transaction_type=None,
            transaction_no=None,
            description=None,
            amount=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Exam('{self.transaction_no}', '{self.amount}')"


class Library(db.Model):
    """ Library Model for storing library related details """
    __tablename__ = "library"

    book_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(), unique=False, nullable=False)
    author = db.Column(db.String(), unique=False, nullable=False)
    book_no = db.Column(db.String(), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(
            self,
            admission_no=None,
            title=None,
            author=None,
            book_no=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.title = title
        self.author = author
        self.book_no = book_no
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Library('{self.title}', '{self.author}')"


class Accommodation(db.Model):
    """ Accommodation Model for storing accommodation related details """
    __tablename__ = "accommodation"

    accommodation_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    hostel = db.Column(db.String(120), db.ForeignKey(
        'hostels.hostel_name', ondelete='CASCADE'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, admission_no=None, hostel_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.hostel_name = hostel_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Accommodation('{self.admission_no}', '{self.hostel_name}')"


class Checklist(db.Model):
    """ Checklist Model for storing checklist related details """
    __tablename__ = "checklist"

    checklist_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    department = db.Column(db.String(120), db.ForeignKey(
        'departments.department_name', ondelete='CASCADE'), nullable=False)
    course = db.Column(db.String(120), db.ForeignKey(
        'courses.courses_name', ondelete='CASCADE'), nullable=False)
    certificate = db.Column(db.Integer, db.ForeignKey(
        'certificates.certificate_id', ondelete='CASCADE'), nullable=False)
    year = db.Column(db.Integer, db.ForeignKey(
        'academic_year.year_id', ondelete='CASCADE'), nullable=False)
    campus = db.Column(db.Integer, db.ForeignKey(
        'campuses.campus_id', ondelete='CASCADE'), nullable=False)
    hostel = db.Column(db.String(120), db.ForeignKey(
        'hostels.hostel_name', ondelete='CASCADE'), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, admission_no=None, department_name=None,
                 course_name=None, certificate_id=None, year_id=None,
                 campus_id=None, hostel_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.department_name = department_name
        self.course_name = course_name
        self.certificate_id = certificate_id
        self.year_id = year_id
        self.campus_id = campus_id
        self.hostel_name = hostel_name
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Checklist('{self.admission_no}', '{self.year_id}')"


class Notification(db.Model):
    """ Notification Model for storing notification related details """
    __tablename__ = "notifications"

    notification_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, subject=None, description=None, created_on=None):
        super().__init__()
        self.subject = subject
        self.description = description
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Notification('{self.subject}', '{self.description}')"
