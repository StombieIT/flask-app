from datetime import datetime
from services.db import db


class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(
		db.Integer,
		primary_key=True
	)
	title = db.Column(
		db.String(64),
		nullable=False
	)
	content = db.Column(
		db.Text,
		nullable=False
	)
	edit = db.Column(
		db.Boolean,
		default=False,
		nullable=False
	)
	publication_datetime = db.Column(
		db.DateTime,
		default=datetime.now(),
		nullable=False,
		index=True
	)
	user_id = db.Column(
		db.Integer,
		db.ForeignKey('users.id'),
		nullable=False
	)

	def __repr__(self):
		return '<Post %r>' % self.id
