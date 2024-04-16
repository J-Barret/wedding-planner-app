"""
BaseTest

This class should be the parent class to each unit test.
It allows for instantiation of the database dynamically,
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import create_app
from db import db

class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///test_data.db"

    @classmethod
    def setUpClass(cls): #runs once for each test case (test class)
        cls.app = create_app(test_db_url=BaseTest.SQLALCHEMY_DATABASE_URI)

    def setUp(self): #runs once for each test method
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
