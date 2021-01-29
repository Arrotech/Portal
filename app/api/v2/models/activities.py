from datetime import datetime
from sqlalchemy import inspect
from app import db


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
