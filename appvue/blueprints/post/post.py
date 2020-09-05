from datetime import datetime
from flask import (
	Blueprint,
	render_template,
	redirect,
	url_for,
	flash,
	abort
)
from flask_login import current_user, login_required
from services.db import db
from .models import Post
from .forms import PostForm

post = Blueprint('post', __name__)


@post.route('/<int:page>/')
def index(page):
	pages = Post.query.order_by(Post.publication_datetime.desc()).paginate(page=page, per_page=3)
	return render_template('post/index.html', page=page)


@post.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(
			title=form.title.data,
			content=form.content.data,
			user_id=current_user.id
		)
		db.session.add(post)
		flash(u'Вы создали пост', 'success')
		return redirect(url_for('post.index', page=1))
	else:
		for errors in form.errors.values():
			for error in errors:
				flash(error, 'danger')
		return render_template('post/create.html', form=form)


@post.route('/view/<int:id>/')
def view(id):
	post = Post.query.get_or_404(id)
	return render_template('post/view.html', id=id)


@post.route('/edit/<int:id>/', methods=['GET', 'POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	if current_user.id == post.user.id:
		form = PostForm()
		if form.validate_on_submit():
			post.title = form.title.data
			post.content = form.content.data
			post.edit = True
			post.publication_datetime = datetime.now()
			db.session.add(post)
			flash(u'Вы отредактировали пост', 'success')
			return redirect(url_for('post.index', page=1))
		else:
			form.content.data = post.content
			for errors in form.errors.values():
				for error in errors:
					flash(error, 'danger')
			return render_template('post/edit.html', form=form, post=post)
	else:
		abort(403)


@post.route('/delete/<int:id>/')
@login_required
def delete(id):
	post = Post.query.get_or_404(id)
	if current_user.id == post.user.id:
		db.session.delete(post)
		flash(u'Вы удалили пост', 'success')
		return redirect(url_for('post.index', page=1))
	else:
		abort(403)
