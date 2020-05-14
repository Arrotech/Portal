import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class HostelsModel(Database):
    """Initiallization."""

    def __init__(self, hostel_name=None, rooms=None, hostel_location=None, date=None):
        super().__init__()
        self.hostel_name = hostel_name
        self.rooms = rooms
        self.hostel_location = hostel_location
        self.date = datetime.now()

    def save(self):
        """Add a new hostel."""
        self.curr.execute(
            ''' INSERT INTO hostels(hostel_name, rooms, hostel_location, date)
            VALUES('{}','{}','{}','{}')
            RETURNING hostel_name, rooms, hostel_location, date'''
            .format(self.hostel_name, self.rooms, self.hostel_location, self.date))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_hostel_by_name(self, hostel_name):
        """Fetch hostel by name."""
        self.curr.execute(
            """ SELECT * FROM hostels WHERE hostel_name=%s""",(hostel_name,),)
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def get_all_hostels(self):
        """Fetch all hostels."""
        self.curr.execute(
            """ SELECT * FROM hostels """)
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response
    
    def get_hostel_by_id(self, hostel_id):
        """Fetch hostel by id."""
        self.curr.execute(
            """ SELECT * FROM hostels WHERE hostel_id={}""".format(hostel_id))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def view_hostel_by_location(self, hostel_location):
        """View hostel(s) by location."""
        self.curr.execute(
            """ SELECT * FROM hostels WHERE hostel_location=%s""",(hostel_location,),)
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
