import json
import psycopg2

from datetime import datetime
from app.api.v1.models.database import Database

Database().create_table()


class FeesModels(Database):
    """Initiallization."""

    def __init__(
            self,
            user_id=None,
            transaction_type=None,
            transaction_no=None,
            description=None,
            amount=None,
            date=None):
        super().__init__()
        self.user_id = user_id
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount
        self.date = datetime.now()

    def save(self):
        """Create a new fee entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO fees(student, transaction_type, transaction_no, description, amount, date)
                VALUES('{}','{}','{}','{}','{}','{}')
                RETURNING student, transaction_type, transaction_no, description, amount, date'''
                .format(self.user_id, self.transaction_type, self.transaction_no, self.description, self.amount, self.date))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_all_fees(self):
        """Fetch all fees"""
        self.curr.execute(''' 
                          SELECT users.admission_no FROM fees
                          INNER JOIN users ON fees.student = users.user_id
                          ''')
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_fee_by_user_id(self, user_id):
        """Get fees for a specific student by his/her id."""
        self.curr.execute(
            """
            SELECT users.admission_no FROM fees
            INNER JOIN users ON fees.student = users.user_id
            WHERE user_id={}
            """.format(user_id))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def edit_fees(self, fee_id, transaction_type, transaction_no, description, amount):
        """Edit fees."""
        self.curr.execute("""UPDATE fees
			SET transaction_type='{}', transaction_no='{}', description='{}', amount='{}'
			WHERE fee_id={} RETURNING transaction_type, transaction_no, description, amount"""
                          .format(fee_id, transaction_type, transaction_no, description, amount))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response
