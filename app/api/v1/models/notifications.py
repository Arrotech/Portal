import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class NotificationsModel(Database):
    """Initiallization."""

    def __init__(self, subject=None, description=None, created_on=None):
        super().__init__()
        self.subject = subject
        self.description = description
        self.created_on = datetime.now()

    def save(self):
        """Add new notification."""
        self.curr.execute(
            ''' INSERT INTO notifications(subject, description, created_on)
            VALUES('{}','{}','{}')
            RETURNING subject, description, created_on'''
            .format(self.subject, self.description, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response