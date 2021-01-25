import json
import psycopg2

from datetime import datetime
from app.api.v1.models.database import Database
from utils.serializer import Serializer

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
            expected_amount=None,
            created_on=None):
        super().__init__()
        self.admission_no = admission_no
        self.transaction_type = transaction_type
        self.transaction_no = transaction_no
        self.description = description
        self.amount = amount
        self.expected_amount = expected_amount
        self.created_on = datetime.now()

    def save(self):
        """Create a new fee entry."""
        self.curr.execute(
            ''' INSERT INTO fees(student, transaction_type, transaction_no,\
            description, amount, expected_amount, created_on)
            VALUES('{}','{}','{}','{}','{}','{}','{}')
            RETURNING student, transaction_type, transaction_no, description,\
            amount, expected_amount, created_on'''
            .format(self.admission_no, self.transaction_type,
                    self.transaction_no, self.description, self.amount,
                    self.expected_amount, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_fees(self):
        """Fetch all fees"""
        query = "SELECT f.transaction_type, f.transaction_no, f.description,\
                f.amount, f.expected_amount, f.created_on, u.admission_no, u.firstname,\
                u.lastname, u.surname FROM fees AS f\
                INNER JOIN users AS u ON f.student = u.admission_no"
        response = Database().fetch(query)
        return response

    def get_fee_by_id(self, fee_id):
        """Fetch fee by Id."""
        query = "SELECT * FROM fees WHERE fee_id=%s"
        response = Database().fetch_one(query, fee_id)
        return response

    def get_fee_by_user_admission(self, admission_no):
        """Get fees for a specific student by his/her admission."""
        self.curr.execute(
            """SELECT f.transaction_type, f.transaction_no, f.description,
            f.amount, f.expected_amount, f.created_on, u.admission_no, u.firstname, u.lastname,\
            u.surname FROM fees AS f
            INNER JOIN users AS u ON f.student = u.admission_no
            WHERE admission_no=%s
            """, (admission_no,))
        response = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return response

    def get_latest_fee_by_admission(self, admission_no):
        """Get the latest fee entry."""
        query = "SELECT f.transaction_type, f.transaction_no, f.description,\
                f.amount, f.expected_amount FROM fees AS f\
                INNER JOIN users AS u ON f.student = u.admission_no\
                WHERE admission_no=%s ORDER BY f.created_on DESC"
        response = Database().fetch_one(query, admission_no)
        return response

    def edit_fees(self, fee_id, transaction_type, transaction_no, description,
                  amount, expected_amount):
        """Edit fees."""
        self.curr.execute("""UPDATE fees\
                            SET transaction_type='{}', transaction_no='{}',\
                            description='{}', amount='{}', expected_amount='{}'\
                            WHERE fee_id={}
                            RETURNING transaction_type, transaction_no,\
                            description, amount, expected_amount"""
                          .format(fee_id, transaction_type, transaction_no,
                                  description, amount, expected_amount))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, fee_id):
        """Delete fee by id."""
        self.curr.execute(
            """DELETE FROM fees WHERE fee_id={}""".format(fee_id))
        self.conn.commit()
        self.curr.close()
