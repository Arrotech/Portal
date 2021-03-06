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

    def get_all_certificates(self):
        """Get all certificates."""
        query = "SELECT * FROM certificates"
        response = Database().fetch(query)
        return response

    def get_certificate_by_id(self, certificate_id):
        """Get ceertificate by id."""
        query = "SELECT * FROM certificates WHERE certificate_id=%s"
        response = Database().fetch_one(query, certificate_id)
        return response

    def edit_certificate(self, certificate_id, certificate_name):
        """Update certificate."""
        self.curr.execute(
            """UPDATE certificates SET certificate_name='{}'\
            WHERE certificate_id={} RETURNING certificate_name"""
            .format(certificate_id, certificate_name))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, certificate_id):
        """Delete certificate by id."""
        self.curr.execute(
            """DELETE FROM certificates WHERE certificate_id={}"""
            .format(certificate_id))
        self.conn.commit()
        self.curr.close()
