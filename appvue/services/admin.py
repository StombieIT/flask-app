from flask import abort, flash, redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from .db import db
from blueprints.auth.models import User, Role
from blueprints.auth.admin import UserModelView, RoleModelView
from blueprints.post.models import Post
from blueprints.post.admin import PostModelView


class IndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_allowed(current_user.role.Permission.MODERATE)

	def inaccessible_callback(self, name, **kwargs):
		if current_user.is_authenticated:
			abort(403)
		else:
			flash(u'Пожалуйста, войдите в аккаунт, чтобы получить доступ к данной странице', 'info')
			return redirect(url_for('auth.login', next=url_for('admin.index')))


admin = Admin(index_view=IndexView(), name='Администрирование', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session, endpoint='users'))
admin.add_view(RoleModelView(Role, db.session, endpoint='roles'))
admin.add_view(PostModelView(Post, db.session, endpoint='posts'))
