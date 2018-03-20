from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import app_config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    migrate = Migrate(app, db)

    from app import models
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from .apis import apis as apis_blueprint
    app.register_blueprint(apis_blueprint)
    

    return app
