from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from services.db import db
from blueprints.post.models import Post


class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(
		db.Integer,
		primary_key=True,
	)
	login = db.Column(
		db.String(64),
		unique=True,
		nullable=False,
	)
	email = db.Column(
		db.String(64),
		unique=True,
		nullable=False,
	)
	password = db.Column(
		db.String(128),
		nullable=False,
	)
	# active = db.Column(
	# 	db.Boolean,
	# 	default=False,
	# 	nullable=False,
	# )
	role_id = db.Column(
		db.Integer,
		db.ForeignKey('roles.id'),
		nullable=False,
	)
	posts = db.relationship(
		'Post',
		backref='user',
		lazy='dynamic'
	)

	def __init__(self, *, login, email, password, role_id=1):
		self.login = login
		self.email = email
		self.password = generate_password_hash(password)[21:]
		self.role_id = role_id

	def __repr__(self):
		return '<User %r>' % self.login

	def check_password(self, password):
		return check_password_hash('pbkdf2:sha256:150000$%s' % self.password, password)

	def generate_token(self, expiration=60*60):
		serializer = Serializer(current_app.config['SECRET_KEY'], expiration)
		return serializer.dumps({'active': self.id})

	def check_token(self, token):
		serializer = Serializer(current_app.config['SECRET_KEY'])
		data = serializer.loads(token)
		if data['active'] == self.id:
			self.active = True
			db.session.add(self)
			return True
		return False

	def is_active(self):
		return self.active

	def is_allowed(self, permission):
		return self.is_authenticated and self.role.permission & permission == permission


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(
		db.Integer,
		primary_key=True,
	)
	name = db.Column(
		db.String(64),
		unique=True,
	)
	permission = db.Column(
		db.Integer,
	)
	users = db.relationship(
		'User',
		backref='role',
		lazy='dynamic',
	)

	def __repr__(self):
		return '<Role %r>' % self.name

	class Permission:
		CREATE_POST = 0x1  # 0b0001
		MODERATE = 0x8  # 0b1000
		ADMINISTER = 0xf  # 0b1111
