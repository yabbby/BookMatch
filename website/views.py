from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("home.html")
@views.route('/about')
def about():
    return render_template('about.html')
@views.route('/cart')
def cart():
    return render_template('cart.html')
@views.route('/review')
def review():
    return render_template('Review.html')
@views.route('/category')
def category():
    return render_template('category.html')
@views.route('/community')
def community():
    return render_template('community.html')


