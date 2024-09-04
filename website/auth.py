from flask import Blueprint, render_template, request, redirect, url_for
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
  return render_template("login.html")
@auth.route('/logout')
def logout():
  return render_template("logout.html")
@auth.route('/signup')
def sign_up():
  return render_template("signup.html")
