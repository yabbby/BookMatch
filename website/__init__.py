from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_strong_random_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)  # Initialize SQLAlchemy with the app

    login_manager = LoginManager()
    login_manager.init_app(app)  # Initialize LoginManager with the app
    login_manager.login_view = 'auth.login'  # Redirect to login route if not logged in

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  # Import User model here to avoid circular import
        return User.query.get(int(user_id))

    with app.app_context():
        try:
            from . import models
            db.create_all()  # Create tables
        except Exception as e:
            print(f"Error creating database tables: {e}")
        
        #from . import models
        #db.create_all()  # Create tables

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")

    return app