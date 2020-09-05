from flask import render_template
from app import app


@app.route('/')
def index():
	return render_template('index/index.html')


@app.errorhandler(404)
def page_not_found(error):
	return render_template('index/page_not_found.html'), 404


@app.errorhandler(403)
def forbidden(error):
	return render_template('index/forbidden.html'), 403
