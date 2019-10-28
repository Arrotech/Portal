"""Unittest module."""
import unittest
import json

from app import exam_app
from app.api.v1.models.database import Database
from utils.dummy import bursar_login, bursar_account, admin_login, admin_account, create_account, user_login


class BaseTest(unittest.TestCase):
    """Class to setup the app and tear down the data model."""

    def setUp(self):
        """Set up the app for testing."""
        Database().destroy_table()
        Database().create_table()
        self.app = exam_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Tear down the data models after the tests run."""
        self.app_context.push()
        Database().destroy_table()

    def get_token(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(create_account),
                            content_type='application/json')
        resp = self.client.post('/api/v1/auth/login', data=json.dumps(user_login),
                            content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_refresh_token(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(create_account),
                            content_type='application/json')
        resp = self.client.post('/api/v1/auth/login', data=json.dumps(user_login),
                            content_type='application/json')
        refresh_token = json.loads(resp.get_data(as_text=True))['refresh_token']
        auth_header = {'Authorization': 'Bearer {}'.format(refresh_token)}
        return auth_header

    def get_admin_token(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(admin_account),
                            content_type='application/json')
        resp = self.client.post('/api/v1/auth/login', data=json.dumps(admin_login),
                            content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_bursar_token(self):
        self.client.post('/api/v1/auth/register', data=json.dumps(bursar_account),
                            content_type='application/json')
        resp = self.client.post('/api/v1/auth/login', data=json.dumps(bursar_login),
                            content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header
