from datetime import datetime
from sqlalchemy import inspect
from app import db


class Notification(db.Model):
    """ Notification Model for storing notification related details """
    __tablename__ = "notifications"

    notification_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(), nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, subject=None, description=None, is_read=None,
                 created_on=None):
        super().__init__()
        self.subject = subject
        self.description = description
        self.is_read = is_read
        self.created_on = datetime.now()

    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        return f"Notification('{self.subject}', '{self.description}')"
