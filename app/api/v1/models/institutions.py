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
        query = "SELECT * FROM institutions"
        response = Database().fetch(query)
        return response

    def get_institution_by_id(self, institution_id):
        """Get institution by id."""
        query = "SELECT * FROM institutions WHERE institution_id=%s"
        response = Database().fetch_one(query, institution_id)
        return response

    def get_institution_name(self, institution_name):
        """Get institution by name."""
        query = "SELECT * FROM institutions WHERE institution_name=%s"
        response = Database().fetch_one(query, institution_name)
        return response

    def edit_institution(self, institution_id, institution_name):
        """Update institution."""
        self.curr.execute(
            """UPDATE institutions SET institution_name='{}' WHERE institution_id={} RETURNING institution_name""".format(institution_id, institution_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, institution_id):
        """Delete institution by id."""
        self.curr.execute(
            """DELETE FROM institutions WHERE institution_id={}""".format(institution_id))
        self.conn.commit()
        self.curr.close()
