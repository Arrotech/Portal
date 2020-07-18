import json

from utils.dummy import new_notification, notification_keys
from .base_test import BaseTest


class TestNotifications(BaseTest):
    """Test notifications endpoints."""

    def test_send_notifications(self):
        """Test that an admin can send a new notification."""
        response1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Notification sent successfully')
        assert response1.status_code == 201

    def test_send_notification_keys(self):
        """Test that an admin cannot send a new notification with invalid json keys."""
        response1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(notification_keys), content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'],
                         'Invalid subject key')
        assert response1.status_code == 400

    def test_get_notifications_by_id(self):
        """Test that an admin can fetch notifications by id."""
        response1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/notifications/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Notifications retrieved successfully')
        assert response2.status_code == 200

    def test_get_non_existing_notifications_by_id(self):
        """Test that an admin cannot fetch non existing notifications by id."""
        response1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification), content_type='application/json',
            headers=self.get_admin_token())
        response2 = self.client.get(
            '/api/v1/notifications/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response2.data.decode())
        self.assertEqual(result['message'],
                         'Notifications not found')
        assert response2.status_code == 404