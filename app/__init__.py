import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CsrfProtect
from ..config import config
from flask_login import LoginManager
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
mail = Mail()
csrf = CsrfProtect()

#SET UP FLASK-LOGIN
login_manager = LoginManager()
LoginManager.session_protection='strong'
login_manager.login_view = 'account.login'

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	db.init_app(app)

	return app
