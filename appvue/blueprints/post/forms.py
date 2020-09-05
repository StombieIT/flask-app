from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
	title = StringField(
		u'Заголовок',
		validators=[
			DataRequired(message=u'Обязательное поле'),
			Length(1, 64, message=u'Длина заголовка должна быть не менее 1 и не более 64 символов')
		]
	)
	content = TextAreaField(
		u'Содержание',
		validators=[
			DataRequired(message=u'Обязательное поле')
		]
	)
	submit = SubmitField(u'Отправить')
