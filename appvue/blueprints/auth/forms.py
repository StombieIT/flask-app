from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, Regexp

LOGIN_RE = r'^[a-z0-9]+$'
PASSWORD_RE = r'^[a-zA-Z0-9`\-=;"\\,.\/~!@#\$%\^&\*\(\)_\+:\|<>\?]+$'


class UserLoginForm(FlaskForm):
	login = StringField(
		u'Логин',
		validators=[
			DataRequired(message=u'Логин обязателен к заполнению'),
			Length(1, 64, message=u'Длина логина должна быть не менее 1 и не более 64 символов'),
			Regexp(LOGIN_RE, message=u'Логин указан некорректно')
		]
	)
	password = PasswordField(
		u'Пароль',
		validators=[
			DataRequired(message=u'Пароль обязателен к заполнению'),
			Length(6, 64, message=u'Длина пароля должна быть не менее 6 и не более 64 символов'),
			Regexp(PASSWORD_RE, message=u'Пароль указан некорректно')
		]
	)
	submit = SubmitField(u'Отправить')


class UserRegisterForm(FlaskForm):
	login = StringField(
		u'Логин',
		validators=[
			DataRequired(message=u'Логин обязателен к заполнению'),
			Length(1, 64, message=u'Длина логина должна быть не менее 1 и не более 64 символов'),
			Regexp(LOGIN_RE, message=u'Логин указан некорректно')
		],
	)
	email = StringField(
		u'Почтовый адрес',
		validators=[
			DataRequired(message=u'Почтовый адрес обязателен к заполнению'),
			Length(1, 64, message=u'Длина почтового адреса должна быть не менее 1 и не более 64 символов'),
			Email(message=u'Почтовый адрес указан некорректно')
		]
	)
	password = PasswordField(
		u'Пароль',
		validators=[
			DataRequired(message=u'Пароль обязателен к заполнению'),
			Length(6, 64, message=u'Длина пароля должна быть не менее 6 и не более 64 символов'),
			Regexp(PASSWORD_RE, message=u'Пароль указан некорректно')
		]
	)
	password_repeat = PasswordField(
		u'Повторный пароль',
		validators=[
			DataRequired(message=u'Повторный пароль обязателен к заполнению'),
			Length(6, 64, message=u'Длина повторного пароля должна быть не менее 6 и не более 64 символов'),
			Regexp(PASSWORD_RE, message=u'Повторный пароль указан некорректно'),
			EqualTo('password', message=u'Пароли должны совпадать')
		]
	)
	submit = SubmitField(u'Отправить')
