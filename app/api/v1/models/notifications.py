from app.api.v1.models.database import Database
from datetime import datetime


class NotificationsModel(Database):
    """Initiallization."""

    def __init__(self, subject=None, description=None, created_on=None):
        super().__init__()
        self.subject = subject
        self.description = description
        self.created_on = datetime.now()

    def save(self):
        """Add new notification."""
        self.curr.execute(
            ''' INSERT INTO notifications(subject, description, created_on)
            VALUES('{}','{}','{}')
            RETURNING subject, description, created_on'''
            .format(self.subject, self.description, self.created_on))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def get_all_notifications(self):
        """Get all notifications."""
        query = "SELECT * FROM notifications"
        response = Database().fetch(query)
        return response

    def get_notitications_by_id(self, notification_id):
        """Get notifications by id."""
        query = "SELECT * FROM notifications WHERE notification_id=%s"
        response = Database().fetch_one(query, notification_id)
        return response

    def update(self, notification_id, subject, description):
        """Edit notification by id."""
        self.curr.execute("""UPDATE notifications SET subject='{}',\
                          description='{}' WHERE notification_id={}
                          RETURNING subject, description"""
                          .format(notification_id, subject, description))
        response = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return response

    def delete(self, notification_id):
        """Delete notification by id."""
        self.curr.execute(
            """DELETE FROM notifications WHERE notification_id={}"""
            .format(notification_id))
        self.conn.commit()
        self.curr.close()
