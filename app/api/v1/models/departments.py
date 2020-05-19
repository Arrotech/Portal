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
                          RETURNING department_name, created_on""".format(self.department_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
    
    def get_department_name(self, department_name):
        """Get department by name."""
        self.curr.execute("""
                          SELECT * FROM departments WHERE department_name=%s
                          """,(department_name,))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response