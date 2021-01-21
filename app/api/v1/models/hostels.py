import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class HostelsModel(Database):
    """Initiallization."""

    def __init__(self, hostel_name=None, rooms=None, gender=None,
                 hostel_location=None, created_on=None):
        super().__init__()
        self.hostel_name = hostel_name
        self.rooms = rooms
        self.gender = gender
        self.hostel_location = hostel_location
        self.created_on = datetime.now()

    def save(self):
        """Add a new hostel."""
        self.curr.execute(
            ''' INSERT INTO hostels(hostel_name, rooms, gender,\
                hostel_location, created_on)
                VALUES('{}','{}','{}','{}','{}')
                RETURNING hostel_name, rooms, gender, hostel_location,\
                created_on'''
            .format(self.hostel_name, self.rooms, self.gender,
                    self.hostel_location, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_hostels(self):
        """Fetch all hostels."""
        query = "SELECT * FROM hostels"
        response = Database().fetch(query)
        return response

    def get_hostel_by_id(self, hostel_id):
        """Fetch hostel by id."""
        query = "SELECT * FROM hostels WHERE hostel_id=%s"
        response = Database().fetch_one(query, hostel_id)
        return response

    def get_hostel_by_name(self, hostel_name):
        """Fetch hostel by name."""
        query = "SELECT * FROM hostels WHERE hostel_name=%s"
        response = Database().fetch_one(query, hostel_name)
        return response

    def view_hostel_by_location(self, hostel_location):
        """View hostel(s) by location."""
        query = "SELECT * FROM hostels WHERE hostel_location=%s"
        response = Database().fetch_one(query, hostel_location)
        return response

    def edit_hostel(self, hostel_id, hostel_name, rooms, gender,
                    hostel_location):
        """Update hostel by id."""
        self.curr.execute(
            """UPDATE hostels SET hostel_name='{}', rooms='{}', gender='{}',\
            hostel_location='{}' WHERE hostel_id={} RETURNING hostel_name,\
            rooms, gender, hostel_location"""
            .format(hostel_id, hostel_name, rooms, gender, hostel_location))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, hostel_id):
        """Delete a hostel by id."""
        self.curr.execute(
            """DELETE FROM hostels WHERE hostel_id={}""".format(hostel_id))
        self.conn.commit()
        self.curr.close()
