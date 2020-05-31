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

    def get_all_campuses(self):
        """Get all campuses."""
        self.curr.execute("""SELECT * FROM campuses""")
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_campus_by_id(self, campus_id):
        """Get campus by id."""
        self.curr.execute(
            """SELECT * FROM campuses WHERE campus_id={}""".format(campus_id))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_campus(self, campus_id, campus_name, campus_location):
        """Update campus."""
        self.curr.execute(
            """UPDATE campuses SET campus_name='{}', campus_location='{}' WHERE campus_id={} RETURNING campus_name, campus_location""".format(campus_id, campus_name, campus_location))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def delete(self, campus_id):
        """Delete campus by id."""
        self.curr.execute(
            """DELETE FROM campuses WHERE campus_id={}""".format(campus_id))
        self.conn.commit()
        self.curr.close()
