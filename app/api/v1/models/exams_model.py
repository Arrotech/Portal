import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class ExamsModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, unit_id=None, marks=None, date=None):
        super().__init__()
        self.user_id = user_id
        self.unit_id = unit_id
        self.marks = marks
        self.date = datetime.now()

    def save(self):
        """Create a new exam entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO exams(student, unit, marks, date)
                VALUES('{}','{}','{}','{}')
                RETURNING student, unit, marks, date'''
                .format(self.user_id, self.unit_id, self.marks, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"