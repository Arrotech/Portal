import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class AccommodationModel(Database):
    """Initiallization."""

    def __init__(self, user_id=None, hostel_id=None, created_on=None):
        super().__init__()
        self.user_id = user_id
        self.hostel_id = hostel_id
        self.created_on = datetime.now()

    def save(self):
        """Book hostel."""
        try:
            self.curr.execute(
                ''' INSERT INTO accommodation(student, hostel, created_on)
                VALUES('{}','{}','{}')
                RETURNING student, hostel, created_on'''
                .format(self.user_id, self.hostel_id, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"
        
        
    def get_booked_hostels(self):
        """Fetch all booked hostels."""
        self.curr.execute("""SELECT u.firstname, u.lastname, u.surname, u.admission_no,
                          h.hostel_name FROM accommodation AS a
                          INNER JOIN users AS u ON a.student=u.user_id
                          INNER JOIN hostels AS h ON a.hostel=h.hostel_id""")
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response
        