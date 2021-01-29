from datetime import datetime
from sqlalchemy import inspect
from app import db


class Fee(db.Model):
    """ Fee Model for storing fee related details """
    __tablename__ = "fees"

    fee_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String(120), db.ForeignKey(
        'users.admission_no', ondelete='CASCADE'), nullable=False)
    transaction_type = db.Column(db.String(), unique=False, nullable=False)
    transaction_no = db.Column(db.String(), unique=True, nullable=False)
    description = db.Column(db.String(), unique=False, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    expected_amount = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(
            self,
            admission_no=None,
            transaction_type=None,
            transaction_no=None,
            description=None,
            amount=None,
            expected_amount=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount
        self.expected_amount = expected_amount
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Exam('{self.transaction_no}', '{self.amount}')"
