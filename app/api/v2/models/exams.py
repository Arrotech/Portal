from datetime import datetime
from sqlalchemy import inspect
from app import db


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
    # exam_type = db.Column(db.String(120), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, year_id=None, admission_no=None, unit_name=None,
                 marks=None, created_on=None):
        super().__init__()
        self.year_id = year_id
        self.admission_no = admission_no
        self.unit_name = unit_name
        self.marks = marks
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Exam('{self.unit_name}', '{self.marks}')"