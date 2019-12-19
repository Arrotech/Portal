import json

from app.api.v1.models.database import Database

Database().create_table()


class FeesModels(Database):
    """Initiallization."""

    def __init__(
            self,
            admission_no=None,
            transaction_type=None,
            transaction_no=None,
            description=None,
            amount=None):
        super().__init__()
        self.admission_no = admission_no
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount

    def save(self):
        """Create a new fee entry."""
        self.curr.execute(
            ''' INSERT INTO fees(admission_no, transaction_type, transaction_no, description, amount)\
            VALUES('{}','{}','{}','{}',{})\
            RETURNING admission_no, transaction_type, transaction_no, description, amount''' \
                .format(self.admission_no, self.transaction_type, self.transaction_no, self.description, self.amount))
        fees = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(fees, default=str)

    def get_all_fees(self):
        """Fetch all comments"""
        self.curr.execute(''' SELECT * FROM fees''')
        fees = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(fees, default=str)

    def get_admission_no(self, admission_no):
        """Get an exam with specific admission no."""
        self.curr.execute(""" SELECT * FROM fees WHERE admission_no=%s""", (admission_no,))
        fees = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return json.dumps(fees, default=str)