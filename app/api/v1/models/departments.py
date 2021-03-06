from datetime import datetime
from app.api.v1.models.database import Database


class DepartmentsModel(Database):
    """Departments model."""

    def __init__(self, department_name=None, created_on=None):
        """Department constructor."""
        super().__init__()
        self.department_name = department_name
        self.created_on = datetime.now()

    def save(self):
        """Add a new department."""
        self.curr.execute("""
                          INSERT INTO departments(department_name, created_on)
                          VALUES('{}','{}')
                          RETURNING department_name, created_on"""
                          .format(self.department_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_department_name(self, department_name):
        """Get department by name."""
        query = "SELECT * FROM departments WHERE department_name=%s"
        response = Database().fetch_one(query, department_name)
        return response

    def get_all_departments(self):
        """Fetch all departments."""
        query = "SELECT * FROM departments"
        response = Database().fetch(query)
        return response

    def get_department_by_id(self, department_id):
        """Fetch a specific department by id."""
        query = "SELECT * FROM departments WHERE department_id=%s"
        response = Database().fetch_one(query, department_id)
        return response

    def edit_department(self, department_id, department_name):
        """Update department name."""
        self.curr.execute(
            """UPDATE departments SET department_name='{}'\
            WHERE department_id={} RETURNING department_name"""
            .format(department_id, department_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, department_id):
        """Delete department by id."""
        self.curr.execute(
            """DELETE FROM departments WHERE department_id={}"""
            .format(department_id))
        self.conn.commit()
        self.curr.close()
