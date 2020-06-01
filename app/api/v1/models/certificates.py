import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class CertificatesModel(Database):
    """Initiallization."""

    def __init__(self, certificate_name=None, created_on=None):
        super().__init__()
        self.certificate_name = certificate_name
        self.created_on = datetime.now()

    def save(self):
        """Add new certificate."""
        self.curr.execute(
            ''' INSERT INTO certificates(certificate_name, created_on)
            VALUES('{}','{}')
            RETURNING certificate_name, created_on'''
            .format(self.certificate_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response