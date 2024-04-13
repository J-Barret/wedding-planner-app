from db import db
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import Relationship

class UserModel(db.Model):

	__tablename__ = "users"
	id = Column(Integer, primary_key=True)
	username = Column(String(80), unique=True, nullable=False)
	password = Column(String, nullable=False) #password will be stored already hashed
	guests = Relationship("GuestModel", back_populates="user", lazy="dynamic") #so the FileModel can do "my_file.user"

	def json(self):
		return {
			"id": self.id,
			"username": self.username,
			"guests": self.guests
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
