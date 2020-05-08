import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class SubjectsModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, unit_id=None, date=None):
        super().__init__()
        self.user_id = user_id
        self.unit_id = unit_id
        self.date= datetime.now()

    def save(self):
        """Create a new orders."""
        try:
            self.curr.execute(
                ''' INSERT INTO subjects(student, unit, date)
                VALUES('{}','{}','{}')
                RETURNING student, unit, date'''
                .format(self.user_id, self.unit_id, self.date))
            subject = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return subject
        except psycopg2.IntegrityError:
            return "error"
