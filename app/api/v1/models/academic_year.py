import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime
from utils.serializer import Serializer


class AcademicYearModel(Database):
    """Initiallization."""

    def __init__(self, year=None, semester=None, created_on=None):
        super().__init__()
        self.year = year
        self.semester = semester
        self.created_on = datetime.now()

    def save(self):
        """Add new academic year."""
        try:
            self.curr.execute(
                ''' INSERT INTO academic_year(year, semester, created_on)
                VALUES('{}','{}','{}')
                RETURNING year, semester, created_on'''
                .format(self.year, self.semester, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_all_academic_years(self):
        """Get all academic years."""
        try:
            query = "SELECT * FROM academic_year"
            response = Database().fetch(query)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_academic_year_by_id(self, year_id):
        """Get a specific academic year by id."""
        try:
            query = "SELECT * FROM academic_year WHERE year_id=%s"
            response = Database().fetch_one(query, year_id)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def get_academic_year_by_year(self, year):
        """Get a specific academic year by year"""
        try:
            query = "SELECT * FROM academic_year WHERE year=%s"
            response = Database().fetch_one(query, year)
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")

    def edit_academic_year(self, year_id, year, semester):
        """Update specific academic year by id."""
        try:
            self.curr.execute(
                """UPDATE academic_year SET year='{}', semester='{}' WHERE year_id={} RETURNING year, semester""".format(year_id, year, semester))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")
    
    def delete(self, year_id):
        """Delete academic year by id."""
        try:
            self.curr.execute(
                """DELETE FROM academic_year WHERE year_id={}""".format(year_id))
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return Serializer.serialize(f"{e}", 500, "Error")
