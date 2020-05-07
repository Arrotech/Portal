import json

from datetime import datetime
from app.api.v1.models.database import Database


class UnitsModel(Database):

    """Initialization."""

    def __init__(self, unit_name=None, unit_code=None, date=None):
        super().__init__()
        self.unit_name = unit_name
        self.unit_code = unit_code
        self.date = datetime.now()

    def save(self):
        """Add a new unit."""
        self.curr.execute(
            ''' INSERT INTO units(unit_name, unit_code, date)\
            VALUES('{}','{}','{}')\
            RETURNING unit_name, unit_code, date'''
            .format(self.unit_name, self.unit_code, self.date))
        unit = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return unit

    def get_units(self):
        """Fetch all availaable units."""
        self.curr.execute("""SELECT * FROM units""")
        units = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return units

    def get_unit_by_id(self, unit_id):
        """Fetch a unit by id."""
        self.curr.execute(
            """ SELECT * FROM units WHERE unit_id={}""".format(unit_id))
        unit = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return unit

    def get_unit_by_name(self, unit_name):
        """Fetch a unit by name."""
        self.curr.execute(
            """ SELECT * FROM units WHERE unit_name=%s""", (unit_name,))
        unit = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return unit

    def get_unit_by_code(self, unit_code):
        """Fetch a unit by code."""
        self.curr.execute(
            """ SELECT * FROM units WHERE unit_code=%s""", (unit_code,))
        unit = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return unit
