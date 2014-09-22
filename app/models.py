from app import db

from hashlib import md5

ROLE_USER=0
ROLE_ADMIN=1
# 
class User(db.Model):
	__table__name = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50), unique= True)
	email = db.Column(db.String(120), unique=True)
	role=db.Column(db.SmallInteger, default=ROLE_USER)
	password=db.Column(db.String(120))

	def __init__(self, name=None, email=None, password=None):
		self.name = name
		self.email = email
		self.password = password

	def is_authenticated(self):
		return True

	def is_activate(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' %(self.name)
		
