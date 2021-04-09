import json

from utils.v1.dummy.streams import add_stream, add_stream_keys
from tests.base_test import BaseTest


class TestStreams(BaseTest):
    """Test streams endpoints."""

    def test_add_stream(self):
        """Test that an admin can add a new stream."""
        response = self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Stream added successfully')
        assert response.status_code == 201

    def test_add_stream_keys(self):
        """An admin cannot add a new stream with invalid json keys."""
        response = self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream_keys),
            content_type='application/json',
            headers=self.get_registrar_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Invalid stream_name key')
        assert response.status_code == 400

    def test_get_all_streams(self):
        """Test that a user can fetch all streams."""
        self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/streams', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Streams retrived successfully')
        assert response.status_code == 200

    def test_get_streams_by_id(self):
        """Test that an admin can fetch stream by id."""
        self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/streams/1', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Stream retrived successfully')
        assert response.status_code == 200

    def test_get_streams_by_name(self):
        """Test that an admin can fetch stream by name."""
        self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/streams/Form 1A', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Stream retrived successfully')
        assert response.status_code == 200

    def test_get_non_existing_stream_by_id(self):
        """Test that an admin cannot fetch non existing stream by id."""
        self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/streams/10', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Stream not found')
        assert response.status_code == 404

    def test_get_non_existing_stream_by_name(self):
        """Test that an admin cannot fetch non existing stream by name."""
        self.client.post(
            '/api/v1/streams', data=json.dumps(add_stream),
            content_type='application/json',
            headers=self.get_registrar_token())
        response = self.client.get(
            '/api/v1/streams/Form 2A', content_type='application/json',
            headers=self.get_token())
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'],
                         'Stream not found')
        assert response.status_code == 404