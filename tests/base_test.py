"""Unittest module."""
import unittest
import json
import os

from app import exam_app
from app.api.v1.models.database import Database
from utils.v1.dummy.accountant_accounts import default_accountant_login, default_accountant_account
from utils.v1.dummy.admin_accounts import default_admin_account, default_admin_login
from utils.v1.dummy.students_accounts import default_student_account, default_student_login
from utils.v1.dummy.registrar import default_registrar_account, default_registrar_login


class BaseTest(unittest.TestCase):
    """Class to setup the app and tear down the data model."""

    def setUp(self):
        """Set up the app for testing."""
        self.app = exam_app("testing")
        self.app.config['SECRET_KEY'] = "schoolportal"
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        Database().destroy_table()
        Database().create_table()

    def tearDown(self):
        """Tear down the data models after the tests run."""
        self.app_context.push()
        Database().destroy_table()

    def get_registrar_token(self):
        self.client.post('/api/v1/registrar/register', data=json.dumps(default_student_account),
                         content_type='application/json')
        resp = self.client.post('/api/v1/staff/login', data=json.dumps(default_student_login),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_admin_token(self):
        self.client.post('/api/v1/staff/register', data=json.dumps(default_admin_account),
                         content_type='application/json', headers=self.get_registrar_token())
        resp = self.client.post('/api/v1/staff/login', data=json.dumps(default_admin_login),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_accountant_token(self):
        self.client.post('/api/v1/accountant/register', data=json.dumps(default_accountant_account),
                         content_type='application/json', headers=self.get_registrar_token())
        resp = self.client.post('/api/v1/accountant/login', data=json.dumps(default_accountant_login),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_token(self):
        self.client.post('/api/v1/students/register', data=json.dumps(default_student_account),
                         content_type='application/json', headers=self.get_admin_token())
        resp = self.client.post('/api/v1/students/login', data=json.dumps(default_student_login),
                                content_type='application/json')
        access_token = json.loads(resp.get_data(as_text=True))['token']
        auth_header = {'Authorization': 'Bearer {}'.format(access_token)}
        return auth_header

    def get_refresh_token(self):
        self.client.post('/api/v1/students/register', data=json.dumps(default_student_account),
                         content_type='application/json', headers=self.get_admin_token())
        resp = self.client.post('/api/v1/students/login', data=json.dumps(default_student_login),
                                content_type='application/json')
        refresh_token = json.loads(resp.get_data(as_text=True))[
            'refresh_token']
        auth_header = {'Authorization': 'Bearer {}'.format(refresh_token)}
        return auth_header


