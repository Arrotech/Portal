from datetime import datetime
from sqlalchemy import inspect
from app import db


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
