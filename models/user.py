from db import db
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import *

class UserModel(db.Model):

	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String(80), unique=True, nullable=False)
	password = Column(String, nullable=False)

	def json(self):
		return {
			"id": self.id,
			"username": self.username
		}

	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
