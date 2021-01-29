from datetime import datetime
from sqlalchemy import inspect
from app import db


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