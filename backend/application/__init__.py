from flask import Flask, session
from flask_login import LoginManager
from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Range
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from application.config import Config
from flask_apscheduler import APScheduler
from flask_caching import Cache
import os


class ComputerIDIn(Schema):
    computer_id = Integer(validate=[Range(min=1, max=26)])


class UsageIn(Schema):
    usage_id = Integer(validate=[Range(min=1)])


db = SQLAlchemy(session_options={"expire_on_commit": False})
login_manager = LoginManager()
apscheduler = APScheduler()
cache = Cache()


def create_app(config_class=Config):
    """
    Initializes the Gamer Time application.
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # sess = Session(app)

    db.init_app(app)
    cache.init_app(app)
    with app.app_context():
        #     # Initialize models
        db.Model.metadata.reflect(bind=db.engine, schema="public")
        from . import models

        # Initialize Login Manager
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login_page'

        # Initialize apscheduler
        apscheduler.init_app(app)
        apscheduler.start()

        # Import parts of our application
        from .home import home
        from .openrec.routes import openrec
        from .auth.routes import auth
        from .staff.routes import staff
        from .sheetshandler.sheets_routes import sheets_page

        # Register Blueprints
        app.register_blueprint(home)

        return app
