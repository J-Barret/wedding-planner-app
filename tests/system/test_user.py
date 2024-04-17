from models.user import UserModel
from tests.base_test import BaseTest
from werkzeug.datastructures import Authorization
from flask_jwt_extended import decode_token, get_jwt_identity
import json
from blocklist import BLOCKLIST


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
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				data = json.loads(request.data)
				self.assertEqual(request.status_code, 200)
				self.assertIn("access_token", data) #assert that response has both tokens
				self.assertIn("refresh_token", data)
				access_token = json.loads(request.data)["access_token"]
				decoded_token = decode_token(access_token)
				self.assertTrue(decoded_token["fresh"]) #assert that login token is a fresh token
				user_id = decoded_token["sub"]
				self.assertEqual(user_id, 1) #it must be '1', since there is only 1 user in the DB in this test

	def test_user_login_wrong_credentials(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "wrong_name", "password": "password1"}) #wrong name
				self.assertEqual(request.status_code, 400)
				self.assertEqual(json.loads(request.data)["message"], "Username not found.")
				request = client.post("/login", json={"name": "name1", "password": "wrong_password"}) #wrong password
				self.assertEqual(request.status_code, 400)
				self.assertEqual(json.loads(request.data)["message"], "Wrong password.")
	def test_refresh_token_ok(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				refresh_token = json.loads(request.data)["refresh_token"]
				auth = Authorization(auth_type="bearer", token=refresh_token)
				request = client.post("/refresh", auth=auth)
				self.assertEqual(request.status_code, 200)
				self.assertIn("access_token", json.loads(request.data))
				access_token = json.loads(request.data)["access_token"]
				decoded_token = decode_token(access_token)
				self.assertFalse(decoded_token["fresh"]) #assert that login token is NOT a fresh token
	def test_refresh_non_valid_token(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				access_token = json.loads(request.data)["access_token"]
				auth = Authorization(auth_type="bearer", token=access_token) #sending access token instead of refresh token
				request = client.post("/refresh", auth=auth)
				self.assertEqual(request.status_code, 401)
	def test_logout(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				access_token = json.loads(request.data)["access_token"]
				auth = Authorization(auth_type="bearer", token=access_token)
				request = client.post("/logout", auth=auth)
				self.assertEqual(request.status_code, 200)
				jti = decode_token(access_token)["jti"]
				self.assertIn(jti, BLOCKLIST) #check that token was added to the blocklist
				#try to access protected endpoint with revoked token
				request = client.delete("/deleteUser", auth=auth, json={"name": "name1", "password": "password1"})
				self.assertEqual(request.status_code, 401)
				self.assertDictEqual(json.loads(request.data), {"description": "The token has been revoked.", "error": "token_revoked"})
	def test_delete_user(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				access_token = json.loads(request.data)["access_token"]
				auth = Authorization(auth_type="bearer", token=access_token)
				request = client.delete("/deleteUser", auth=auth, json={"name": "wrong_name", "password": "password1"})
				self.assertEqual(request.status_code, 400)
				self.assertEqual(json.loads(request.data)["message"], "Username not found.")
				request = client.delete("/deleteUser", auth=auth, json={"name": "name1", "password": "password1"})
				self.assertEqual(request.status_code, 200)
				self.assertEqual(json.loads(request.data)["message"], "User deleted.")

	def test_delete_user_stale_token(self):
		with self.client as client:
			with self.app_context():
				client.post("/register", json={"name": "name1", "password": "password1"})
				request = client.post("/login", json={"name": "name1", "password": "password1"})
				refresh_token = json.loads(request.data)["refresh_token"]
				auth = Authorization(auth_type="bearer", token=refresh_token)
				request = client.post("/refresh", auth=auth)
				new_access_token = json.loads(request.data)["access_token"]
				auth = Authorization(auth_type="bearer", token=new_access_token)
				request = client.delete("/deleteUser", auth=auth, json={"name": "name1", "password": "password1"})
				self.assertEqual(request.status_code, 401)
				self.assertDictEqual(json.loads(request.data), {"description": "The token is not fresh.",
																	"error": "fresh_token_required"})

