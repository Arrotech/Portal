from datetime import datetime
from sqlalchemy import inspect
from app import db


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