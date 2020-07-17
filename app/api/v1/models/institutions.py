import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class InstitutionsModel(Database):
    """Initiallization."""

    def __init__(self, institution_name=None, created_on=None):
        super().__init__()
        self.institution_name = institution_name
        self.created_on = datetime.now()

    def save(self):
        """Add new institution."""
        self.curr.execute(
            ''' INSERT INTO institutions(institution_name, created_on)
            VALUES('{}','{}')
            RETURNING institution_name, created_on'''
            .format(self.institution_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_institutions(self):
        """Get all institutions."""
        self.curr.execute("""SELECT * FROM institutions""")
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response