from datetime import datetime
from sqlalchemy import inspect
from app import db


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