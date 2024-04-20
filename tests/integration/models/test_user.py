from models.user import UserModel
from models.guest import GuestModel
from tests.base_test import BaseTest

class UserTest(BaseTest):

	def test_create_delete_user(self):
		with self.app_context():
			user = UserModel("username1", "password1")
			self.assertIsNone(UserModel.find_by_username("username1")) #check that it does not exist in DB before saving it
			user.save_to_db()
			self.assertIsNotNone(UserModel.find_by_username("username1"))
			user.delete_from_db()
			self.assertIsNone(UserModel.find_by_username("username1"))
	def test_find_in_db(self):
		with self.app_context():
			user = UserModel("username1", "password1")
			user.save_to_db()
			result = UserModel.find_by_username("wrong_username")
			self.assertIsNone(result)
			result = UserModel.find_by_username("username1")
			self.assertIsNotNone(result)
			self.assertEqual(result, user)
	def test_foreign_keys(self):
		with self.app_context():
			user = UserModel("username1", "password1")
			user.save_to_db() #important to do this in this order, so SQL assigns user.id value (nullable=False in GuestModel)
			guest1 = GuestModel("guest1", "number1", "email1", user.id, "wedding_id1")
			guest2 = GuestModel("guest2", "number2", "email2", user.id, "wedding_id1")
			guest1.save_to_db()
			guest2.save_to_db()
			self.assertEqual(guest1.user, user)
			self.assertEqual(guest2.user, user)
			self.assertEqual(user.guests.all(), [guest1, guest2])
