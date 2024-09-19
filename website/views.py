from flask import Blueprint, render_template, request, redirect, url_for, flash , jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Review
from .models import User
from .models import Contact
from . import db


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    reviewer_name = "Default Reviewer"
    if request.method == 'POST':
        title = request.form.get('title')
        reviewer = request.form.get('reviewer')
        author = request.form.get('author')
        image = request.form.get('image')
        rating = request.form.get('rating')
        review_content = request.form.get('review')

        if current_user.is_authenticated:  # Check if the user is authenticated
            user_id = current_user.id
        else:
            flash('You must be logged in to submit a review.', category='error')
            return redirect(url_for('views.review'))

        # Create the new review object
        if reviewer_name is None:
            reviewer_name = "Default Reviewer"
        else:
            reviewer_name = reviewer

        new_review = Review(
            title=title,
            reviewer=reviewer,
            author=author,
            image=image,
            rating=rating,
            review=review_content,
            user_id=user_id
        )

        # Store the new review (only once)
        db.session.add(new_review)
        db.session.commit()
        flash('Review submitted successfully!', category='success')
        return redirect(url_for('views.review'))

    reviews = Review.query.all()
    return render_template('review.html', reviews=reviews)
#for deleting reviews
@views.route('/delete_review', methods=['POST'])
def delete_review():
    review_id = request.form.get('review_id')
    review = Review.query.get(review_id)
    if review:
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted successfully!')
        return redirect(url_for('review_list'))  # Redirect to your review list page
    else:
        flash('Review not found.')
        return redirect(url_for('review_list'))

@views.route('/category', methods=['GET', 'POST'])
def category():
    return render_template('category.html')

@views.route('/blogs')
def blogs():
    return render_template('blogs.html')

@views.route('/contact', methods=['GET', 'POST'])
def contact():       
    return render_template('contact.html')

@views.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@views.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')
#user profile
@views.route('/profile', methods=['GET', 'POST'])
@views.route('/users')
def view_users():
    users = User.query.all()  # Fetch all users from the database
    return render_template("view_users.html", users=users)

#edit user
@views.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required  # Protect this route
def edit_user(user_id):
    user = User.query.get_or_404(user_id)  # Retrieve the user or return a 404 error

    if request.method == 'POST':
        user.email = request.form.get('email')
        user.first_name = request.form.get('first_name')
        # Optionally update the password if provided
        if request.form.get('password'):
            user.password = generate_password_hash(request.form.get('password'))

        db.session.commit()  # Save changes to the database
        flash('User updated successfully!', category='success')
        return redirect(url_for('views.view_users'))  # Redirect back to the users page

    return render_template("edit_user.html", user=user)


#delete user
@views.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required  # Protect this route
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  # Retrieve the user or return a 404 error
    db.session.delete(user)  # Delete the user from the database
    db.session.commit()  # Commit the changes to the database
    flash('User deleted successfully!', category='success')
    return redirect(url_for('views.view_users'))  # Redirect back to the users page

