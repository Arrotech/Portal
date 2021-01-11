import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime
from utils.serializer import Serializer


class AccommodationModel(Database):
    """Initiallization."""

    def __init__(self, admission_no=None, hostel_name=None, created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.hostel_name = hostel_name
        self.created_on = datetime.now()

    def save(self):
        """Book hostel."""
        self.curr.execute(
            ''' INSERT INTO accommodation(student, hostel, created_on)
            VALUES('{}','{}','{}')
            RETURNING student, hostel, created_on'''
            .format(self.admission_no, self.hostel_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_booked_hostels(self):
        """Fetch all booked hostels."""
        query = "SELECT u.firstname, u.lastname, u.surname, u.admission_no, h.hostel_name FROM accommodation AS a INNER JOIN users AS u ON a.student=u.admission_no INNER JOIN hostels AS h ON a.hostel=h.hostel_name"
        response = Database().fetch(query)
        return response

    def get_booked_hostel_by_id(self, accommodation_id):
        """Get specific booked hostle by id."""
        query = "SELECT * FROM accommodation WHERE accommodation_id=%s"
        response = Database().fetch_one(query, accommodation_id)
        return response

    def get_booked_hostel_by_admission(self, admission_no):
        """Fetch booked hostel by admission."""
        query = "SELECT u.firstname, u.lastname, u.surname, u.admission_no, h.hostel_name FROM accommodation AS a INNER JOIN users AS u ON a.student=u.admission_no INNER JOIN hostels AS h ON a.hostel=h.hostel_name WHERE admission_no=%s"
        response = Database().fetch_one(query, admission_no)
        return response

    def get_accommodation_history_by_admission_no(self, admission_no):
        """Get accommodation history by admission number."""
        query = "SELECT * FROM accommodation WHERE student=%s"
        response = Database().fetch_group(query, admission_no)
        return response

    def update(self, accommodation_id, hostel_name):
        """Update specific hostel by id."""
        self.curr.execute(
            """UPDATE accommodation SET hostel='{}' WHERE accommodation_id={} RETURNING hostel""".format(accommodation_id, hostel_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, accommodation_id):
        """Delete hostel by id."""
        self.curr.execute(
            """DELETE FROM accommodation WHERE accommodation_id={}""".format(accommodation_id))
        self.conn.commit()
        self.curr.close()
