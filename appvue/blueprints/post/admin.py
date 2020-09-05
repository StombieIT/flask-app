from flask import (
	abort,
	flash,
	redirect,
	url_for
)
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class PostModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_allowed(current_user.role.Permission.MODERATE)

	def inaccessible_callback(self, name, **kwargs):
		if current_user.is_authenticated:
			abort(403)
		else:
			flash(u'Пожалуйста, войдите в аккаунт, чтобы получить доступ к данной странице', 'info')
			return redirect(url_for('auth.login', next=url_for('admin.index')))
