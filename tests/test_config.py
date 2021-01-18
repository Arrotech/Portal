import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('instance.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
                'DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('instance.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] == 'my_precious')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
                'TEST_DATABASE_URL')
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('instance.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
