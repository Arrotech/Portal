from datetime import datetime
from sqlalchemy import inspect
from app import db


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
