from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint('auth', __name__)

# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', category='success')
            return redirect(url_for('views.home'))  
        else:
            flash('Login failed. Check your email and/or password.', category='error')

    return render_template("login.html")




# Logout page
@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash('You have been logged out.', category='success')
    return redirect(url_for('views.home')) 



# Signup page
@auth.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')

        if not email or not password or not first_name:
            flash('Please fill out all fields.', category='error')
            return redirect(url_for('auth.sign_up'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already exists. Please choose a different one.', category='error')
            return redirect(url_for('auth.sign_up'))

        # Hash the password using the default method
        new_user = User(
            email=email,
            password=generate_password_hash(password),  # Default hashing
            first_name=first_name
        )
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', category='success')
        return redirect(url_for('auth.login'))  # Redirect to login page after signup

    return render_template("signup.html")

# Display all registered users
@auth.route('/registered')
@login_required
def registered():
    users = User.query.all()  # Get all users from the database
    return render_template("registered.html", users=users)