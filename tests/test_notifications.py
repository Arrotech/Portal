import json

from utils.v1.dummy.notifications import new_notification, notification_keys,\
    update_notification_keys, update_notification
from tests.base_test import BaseTest


class TestNotifications(BaseTest):
    """Test notifications endpoints."""

    def test_send_notifications(self):
        """Test that an admin can send a new notification."""
        response = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification sent successfully')
        assert response.status_code == 201

    def test_send_notification_keys(self):
        """An admin cannot send a notification with invalid json keys."""
        response = self.client.post(
            '/api/v1/notifications', data=json.dumps(notification_keys),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid subject key')
        assert response.status_code == 400

    def test_get_all_notifications(self):
        """Test that an admin can fetch all notifications."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/notifications', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notifications retrieved successfully')
        assert response.status_code == 200

    def test_get_latest_notifications(self):
        """Test that a user can fetch latest notifications."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/notifications/latest', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notifications retrieved successfully')
        assert response.status_code == 200

    def test_get_notifications_by_id(self):
        """Test that an admin can fetch notifications by id."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/notifications/1', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification retrieved successfully')
        assert response.status_code == 200

    def test_get_non_existing_notifications_by_id(self):
        """Test that an admin cannot fetch non existing notifications by id."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.get(
            '/api/v1/notifications/10', content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification not found')
        assert response.status_code == 404

    def test_update_notification(self):
        """Test that an admin can update a notification."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.put(
            '/api/v1/notifications/1', data=json.dumps(update_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification updated successfully')
        assert response.status_code == 200

    def test_update_notification_keys(self):
        """Test that an admin cannot update a notification with wrong keys."""
        r1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        print(r1.data)
        response = self.client.put(
            '/api/v1/notifications/1', data=json.dumps(update_notification_keys),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid subject key')
        assert response.status_code == 400

    def test_update_non_existing_notification(self):
        """Test that an admin cannot update non-existing notification."""
        r1 = self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        print(r1.data)
        response = self.client.put(
            '/api/v1/notifications/100', data=json.dumps(update_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification not found')
        assert response.status_code == 404

    def test_delete_notification(self):
        """Test that an admin can delete a notification."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/notifications/1',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification deleted successfully')
        assert response.status_code == 200

    def test_delete_non_existing_notification(self):
        """Test that an admin cannot delete non-existing notification."""
        self.client.post(
            '/api/v1/notifications', data=json.dumps(new_notification),
            content_type='application/json',
            headers=self.get_admin_token())
        response = self.client.delete(
            '/api/v1/notifications/100',
            content_type='application/json',
            headers=self.get_admin_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Notification not found')
        assert response.status_code == 404
