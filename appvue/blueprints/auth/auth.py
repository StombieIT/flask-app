# -*- coding: utf-8 -*-
from flask import (
	Blueprint,
	render_template,
	redirect,
	url_for,
	flash,
	request,
	abort,
	current_app
)
from flask_login import (
	login_user,
	login_required,
	logout_user,
	current_user
)
from flask_mail import Message
from services.login_manager import login_manager
from services.db import db
from services.mail import mail
from .forms import UserLoginForm, UserRegisterForm
from .models import User

auth = Blueprint('auth', __name__)

login_manager.login_view = 'auth.login'
login_manager.login_message = u'Пожалуйста, войдите в аккаунт, чтобы получить доступ к данной странице'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))


@auth.route('/logout/')
@login_required
def logout():
	logout_user()
	flash(u'Вы вышли с аккаунта', 'success')
	return redirect(url_for('auth.login'))


@auth.route('/login/', methods=['GET', 'POST'])
def login():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter(User.login == form.login.data).first()
		if user is not None and user.check_password(form.password.data):
			login_user(user, True)
			flash(u'Вы вошли в аккаунт', 'success')
			return redirect(request.args.get('next') or url_for('index'))
		else:
			flash(u'Не удаётся войти', 'danger')
			return redirect(url_for('auth.login', next=request.args.get('next')))
	else:
		for errors in form.errors.values():
			for error in errors:
				flash(error, 'danger')
		return render_template('auth/login.html', form=form)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
	form = UserRegisterForm()
	if form.validate_on_submit():
		user = User.query.filter(
			User.login == form.login.data
			or User.email == form.email.data
		).first()
		if user is not None:
			flash(u'Аккаунт с указанными логином или почтовым адресом уже существует', 'danger')
			return redirect(url_for('auth.register'))
		user = User(
			login=form.login.data,
			email=form.email.data,
			password=form.password.data,
		)
		db.session.add(user)
		flash(u'Вы зарегистрировались', 'success')
		return redirect(url_for('index'))
		# db.session.commit()
		# token = user.generate_token()
		# message = Message(
		# 	u'Подтверждение регистрации',
		# 	html=render_template(
		# 		'auth/mail.html',
		# 		login=form.login.data,
		# 		link=url_for('auth.activate', token=token, _external=True)
		# 	),
		# 	recipients=[form.email.data],
		# )
		# with current_app.app_context():
		# 	mail.send(message)
		# flash(u'Письмо с подтверждением регистрации было отправлено на {e}'.format(e=form.email.data), 'info')
		# return redirect(url_for('auth.login'))
	else:
		for errors in form.errors.values():
			for error in errors:
				flash(error, 'danger')
		return render_template('auth/register.html', form=form)


@auth.route('/activate/<token>/')
@login_required
def activate(token):
	if current_user.is_active():
		flash(u'Вы уже подтвердили регистрацию', 'info')
		return redirect(url_for('index'))
	elif current_user.check_token(token):
		flash(u'Вы подтвердили регистрацию', 'success')
		return redirect(url_for('auth.login'))
	else:
		abort(404)
