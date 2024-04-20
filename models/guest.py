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
	user = Relationship("UserModel", back_populates="guests") #so the UserModel can do "my_user.guests"
	status = Column(Enum("Pending", "Confirmed", "Declined"), unique=False, nullable=False)
	wedding_id = Column(Integer, unique=False, nullable=False) #several guests will have same wedding ID

	def __init__(self, name, number, email, user_id, wedding_id):
		self.name = name
		self.number = number
		self.email = email
		self.user_id = user_id
		self.status = "Pending" #default init value
		self.wedding_id = wedding_id

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
