from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'your_strong_random_secret_key'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/auth')

  return app
