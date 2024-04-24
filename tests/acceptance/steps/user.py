from behave import *
from models.user import UserModel
import json

use_step_matcher("re")

@given("There are no other users with the same name")
def step_impl(context):
	with context.client as client:
		with context.app_context():
			assert UserModel.find_by_username("username1") is None

@when("I send correct register credentials")
def step_impl(context):
	with context.client as client:
		with context.app_context():
			context.response = client.post("/register", json={"name": "username1", "password": "password1"})

@then("I successfully register a new user")
def step_impl(context):
	assert context.response.status_code == 201
	assert json.loads(context.response.data)["message"] == "User created succesfully."