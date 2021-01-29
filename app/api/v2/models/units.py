from datetime import datetime
from sqlalchemy import inspect
from app import db


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
