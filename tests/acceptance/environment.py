"""
The environment.py file in Behave serves as the entry point for defining hooks and setting up the testing environment
for your Gherkin feature files. It allows you to define global setup and teardown logic that applies to all scenarios.
"""

from app import create_app
from db import db


def before_scenario(context, scenario): #these run before each scenario is run
    context.test_db_uri = "sqlite:///test_data.db"
    context.app = create_app(test_db_url=context.test_db_uri)
    with context.app.app_context():
        db.create_all()
    context.client = context.app.test_client()
    context.app_context = context.app.app_context

def after_scenario(context, scenario): #these run after each scenario is run
    with context.app.app_context():
        db.session.remove()
        db.drop_all()