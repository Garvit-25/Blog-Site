from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_material import Material

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:25012001@localhost/blogSiteDB'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '968331509722a24aaca4a6ab62dea0cd'

db = SQLAlchemy(app)
Migrate(app,db)
Material(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


from blogSite.core.routes import core
from blogSite.error_pages.handlers import error_pages
from blogSite.users.routes import users
from blogSite.blog_posts.routes import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)