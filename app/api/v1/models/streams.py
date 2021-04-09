import json
import psycopg2

from app.api.v1.models.database import Database
from datetime import datetime


class StreamsModel(Database):
    """Initiallization."""

    def __init__(self, stream_name=None, created_on=None):
        super().__init__()
        self.stream_name = stream_name
        self.created_on = datetime.now()

    def save(self):
        """Add a new stream."""
        self.curr.execute(
            ''' INSERT INTO class_streams(stream_name, created_on)
                VALUES('{}','{}')
                RETURNING stream_name, created_on'''
            .format(self.stream_name, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_streams(self):
        """Fetch all class streams."""
        query = "SELECT * FROM class_streams"
        response = Database().fetch(query)
        return response

    def get_stream_by_id(self, stream_id):
        """Fetch stream by id."""
        query = "SELECT * FROM class_streams WHERE stream_id=%s"
        response = Database().fetch_one(query, stream_id)
        return response

    def get_stream_by_name(self, stream_name):
        """Fetch stream by name."""
        query = "SELECT * FROM class_streams WHERE stream_name=%s"
        response = Database().fetch_one(query, stream_name)
        return response
