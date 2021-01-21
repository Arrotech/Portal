from datetime import datetime
from app.api.v1.models.database import Database


class UnitsModel(Database):

    """Initialization."""

    def __init__(self, unit_name=None, unit_code=None, created_on=None):
        super().__init__()
        self.unit_name = unit_name
        self.unit_code = unit_code
        self.created_on = datetime.now()

    def save(self):
        """Add a new unit."""
        self.curr.execute(
            ''' INSERT INTO units(unit_name, unit_code, created_on)\
            VALUES('{}','{}','{}')\
            RETURNING unit_name, unit_code, created_on'''
            .format(self.unit_name, self.unit_code, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_units(self):
        """Fetch all availaable units."""
        query = "SELECT * FROM units"
        response = Database().fetch(query)
        return response

    def get_unit_by_id(self, unit_id):
        """Fetch a unit by id."""
        query = "SELECT * FROM units WHERE unit_id=%s"
        response = Database().fetch_one(query, unit_id)
        return response

    def get_unit_by_name(self, unit_name):
        """Fetch a unit by name."""
        query = "SELECT * FROM units WHERE unit_name=%s"
        response = Database().fetch_one(query, unit_name)
        return response

    def get_unit_by_code(self, unit_code):
        """Fetch a unit by code."""
        query = "SELECT * FROM units WHERE unit_code=%s"
        response = Database().fetch_one(query, unit_code)
        return response

    def delete(self, unit_id):
        """Delete a unit by id."""
        self.curr.execute(
            """DELETE FROM units WHERE unit_id={}""".format(unit_id))
        self.conn.commit()
        self.curr.close()

    def edit(self, unit_id, unit_name, unit_code):
        """Update a unit by id."""
        self.curr.execute(
            """UPDATE units SET unit_name='{}', unit_code='{}' WHERE unit_id={}
            RETURNING unit_name, unit_code"""
            .format(unit_id, unit_name, unit_code))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_name(self, unit_id, unit_name):
        """Update a unit name by id."""
        self.curr.execute(
            """UPDATE units SET unit_name='{}' WHERE unit_id={}
            RETURNING unit_name""".format(unit_id, unit_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_code(self, unit_id, unit_code):
        """Update a unit code by id."""
        self.curr.execute(
            """UPDATE units SET unit_code='{}' WHERE unit_id={}
            RETURNING unit_code""".format(unit_id, unit_code))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
