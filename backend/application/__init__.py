from flask import Flask, session
from apiflask import APIFlask
from flask_login import LoginManager
from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Range
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
from flask_apscheduler import APScheduler
from flask_httpauth import HTTPTokenAuth
import os


class ComputerIDIn(Schema):
    computer_id = Integer(validate=[Range(min=1, max=26)])


db = SQLAlchemy(session_options={"expire_on_commit": False})
login_manager = LoginManager()
apscheduler = APScheduler()
auth = HTTPTokenAuth


def create_app(config_class=DevelopmentConfig):
    """
    Initializes the Gamer Time application.
    """
    app = APIFlask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)

    # sess = Session(app)

    db.init_app(app)
    with app.app_context():
        # Initialize models
        from .models import Usage, ComputerStatus, Player, User
        db.create_all()

        # Initialize Login Manager
        login_manager.init_app(app)
        # login_manager.login_view = 'auth.login_page'

        # Initialize apscheduler
        apscheduler.init_app(app)
        apscheduler.start()

        # Import parts of our application
        from application.esports import esports_bp
        from application.openrec import openrec_bp
        from application.auth import auth_bp

        # from .home import home
        # from .openrec.routes import openrec
        # from .auth.routes import auth
        # from .staff.routes import staff
        # from .sheetshandler.sheets_routes import sheets_page

        # Register Blueprints
        # app.register_blueprint(home)
        app.register_blueprint(esports_bp)
        app.register_blueprint(openrec_bp)
        app.register_blueprint(auth_bp)

        return app
