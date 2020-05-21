import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class AccommodationModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, hostel_id=None, created_on=None):
        super().__init__()
        self.user_id = user_id
        self.hostel_id = hostel_id
        self.created_on = datetime.now()

    def save(self):
        """Book hostel."""
        try:
            self.curr.execute(
                ''' INSERT INTO accommodation(student, hostel, created_on)
                VALUES('{}','{}','{}')
                RETURNING student, hostel, created_on'''
                .format(self.user_id, self.hostel_id, self.created_on))
            subject = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return subject
        except psycopg2.IntegrityError:
            return "error"