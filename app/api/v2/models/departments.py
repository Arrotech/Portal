from datetime import datetime
from sqlalchemy import inspect
from app import db


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