from flask import Flask
import settings
from services.admin import admin
from services.login_manager import login_manager
from services.mail import mail
from services.db import db
from services.migrate import migrate
from blueprints.api.api import api
from blueprints.auth.auth import auth
from blueprints.post.post import post

app = Flask(__name__)
app.config.from_object(settings)

# Apps
admin.init_app(app)
login_manager.init_app(app)
mail.init_app(app)
db.init_app(app)
migrate.init_app(app, db)

# Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(post, url_prefix='/post')
app.register_blueprint(api, url_prefix='/api')