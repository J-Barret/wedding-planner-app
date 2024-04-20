from tests.base_test import BaseTest
from models.guest import GuestModel

class GuestTest(BaseTest):

	def test_create_delete_guest(self):
		with self.app_context():
			guest1 = GuestModel("guest1", "number1", "email1", "1", "wedding_id1")
			self.assertIsNone(GuestModel.find_by_name("guest1"))
			guest1.save_to_db()
			result = GuestModel.find_by_name("guest1")
			self.assertIsNotNone(result)

	def test_find_in_db(self):
		with self.app_context():
			guest1 = GuestModel("guest1", "number1", "email1", "1", "wedding_id1")
			self.assertIsNone(GuestModel.find_by_name("guest1"))
			guest1.save_to_db()
			result_nok = GuestModel.find_by_name("wrong_name")
			result_ok = GuestModel.find_by_name("guest1")
			self.assertIsNone(result_nok)
			self.assertEqual(guest1, result_ok)

