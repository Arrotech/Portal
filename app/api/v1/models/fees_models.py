import json
import psycopg2

from datetime import datetime
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
            amount=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount
        self.created_on = datetime.now()

    def save(self):
        """Create a new fee entry."""
        try:
            self.curr.execute(
                ''' INSERT INTO fees(student, transaction_type, transaction_no, description, amount, created_on)
                VALUES('{}','{}','{}','{}','{}','{}')
                RETURNING student, transaction_type, transaction_no, description, amount, created_on'''
                .format(self.admission_no, self.transaction_type, self.transaction_no, self.description, self.amount, self.created_on))
            response = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return response
        except psycopg2.IntegrityError:
            return "error"

    def get_all_fees(self):
        """Fetch all fees"""
        self.curr.execute(''' SELECT f.transaction_type, f.transaction_no, f.description,
                          f.amount, f.created_on, u.admission_no, u.firstname, u.lastname, u.surname FROM fees AS f
                          INNER JOIN users AS u ON f.student = u.admission_no
                          ''')
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_fee_by_user_admission(self, admission_no):
        """Get fees for a specific student by his/her admission."""
        self.curr.execute(
            """SELECT f.transaction_type, f.transaction_no, f.description,
            f.amount, f.created_on, u.admission_no, u.firstname, u.lastname, u.surname FROM fees AS f
            INNER JOIN users AS u ON f.student = u.admission_no
            WHERE admission_no=%s
            """, (admission_no,))
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
