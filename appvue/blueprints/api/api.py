from flask import Blueprint, jsonify, request, url_for
from flask_login import current_user
from blueprints.auth.models import User
from blueprints.post.models import Post

api = Blueprint('api', __name__)


@api.route('/posts/<int:page>/', methods=['GET'])
def posts(page):
	page_ = Post.query.order_by(Post.publication_datetime.desc()).paginate(page=page, per_page=3)
	page_json = {
		'page': page,
		'prev_url': url_for('api.posts', page=page_.prev_num) if page_.has_prev else False,
		'next_url': url_for('api.posts', page=page_.next_num) if page_.has_next else False,
		'current_user_create_post_url_if_authenticated': url_for('post.create') if current_user.is_authenticated else False,
		'posts': [
			{
				'title': post.title,
				'edit': post.edit,
				'user_login': post.user.login,
				'view_url': url_for('post.view', id=post.id),
				'edit_url': url_for('post.edit', id=post.id),
				'delete_url': url_for('post.delete', id=post.id),
				'current_user_is_allowed_to_change': current_user.is_authenticated and current_user.id == post.user.id
			}
			for post in page_.items
		]
	}
	return jsonify(page_json)


@api.route('/post/<int:id>/')
def post(id):
	post = Post.query.get_or_404(id)
	post_json = {
		'id': post.id,
		'title': post.title,
		'content': post.content,
		'edit': post.edit,
		'publication': {
			'date': post.publication_datetime.strftime('%d.%m.%Y'),
			'time': post.publication_datetime.strftime('%H:%M:%S')
		},
		'user_login': post.user.login
	}
	return jsonify(post_json)
