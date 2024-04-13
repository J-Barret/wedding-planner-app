from db import db
from sqlalchemy import Column, ForeignKey
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import Relationship

class GuestModel(db.Model):

	__tablename__ = "guests"
	id = Column(Integer, primary_key=True)
	name = Column(String(80), unique=False, nullable=False)
	number = Column(String(9), unique=False, nullable=False) #same guest may be in many weddings (unlikely but...)
	email = Column(String(80), unique=False, nullable=True) #mail is optional
	user_id = Column(String, ForeignKey("users.id"), unique=False, nullable=False)
	user = Relationship("UserModel", back_populates="guests") #so the UserModel can do "my_user.files"

	def json(self):
		return {
			"id": self.id,
			"name": self.name,
			"number": self.number,
			"email": self.email,
			"user_id": self.user_id,
			"user": self.user
		}

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()