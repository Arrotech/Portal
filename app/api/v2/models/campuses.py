from datetime import datetime
from sqlalchemy import inspect
from app import db


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