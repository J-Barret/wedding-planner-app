from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
	def test_user_schema_validation_fail(self):
		with self.client as client:
			with self.app_context():
				request = client.post("/register", json={"invalid_field": "value"})
				self.assertEqual(request.status_code, 422) #assert that the status code is 422 (Unprocessable Entity)
	def test_register_user(self):
		with self.client as client:
			with self.app_context():
				request = client.post("/register", json={"name": "name1", "password": "password1"})
				self.assertEqual(request.status_code, 201)
				self.assertIsNotNone(UserModel.find_by_username("name1"))
				self.assertEqual(json.loads(request.data)["message"],"User created succesfully.")
	def test_register_user_already_exists(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/register", json={"name": "name1", "password": "password1"})
				self.assertEqual(request.status_code, 400)
				self.assertEqual(json.loads(request.data)["message"], "Username already exists. Please try another one.")
	def test_user_login_ok(self):
		pass
	def test_user_login_wrong_username(self):
		pass
	def test_user_login_wrong_password(self):
		pass