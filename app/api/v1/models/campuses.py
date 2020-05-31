import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class CampusModel(Database):
    """Initiallization."""

    def __init__(self, campus_name=None, campus_location=None, created_on=None):
        super().__init__()
        self.campus_name = campus_name
        self.campus_location = campus_location
        self.created_on = datetime.now()

    def save(self):
        """Add new campus."""
        self.curr.execute(
            ''' INSERT INTO campuses(campus_name, campus_location, created_on)
            VALUES('{}','{}','{}')
            RETURNING campus_name, campus_location, created_on'''
            .format(self.campus_name, self.campus_location, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response