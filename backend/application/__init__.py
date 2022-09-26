from apiflask import APIFlask
from apiflask import Schema
from apiflask.fields import Integer
from apiflask.validators import Range
from flask_sqlalchemy import SQLAlchemy
from config import ProductionConfig, DevelopmentConfig
from flask_apscheduler import APScheduler
from flask_httpauth import HTTPTokenAuth
from flask_jwt_extended import JWTManager


class ComputerIDIn(Schema):
    computer_id = Integer(validate=[Range(min=1, max=26)])


db = SQLAlchemy(session_options={"expire_on_commit": False})
apscheduler = APScheduler()
auth = HTTPTokenAuth()
jwt = JWTManager()


def create_app():
    """
    Initializes the Gamer Time application.
    """
    app = APIFlask(__name__, static_folder='react-app/build',
                   instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)
    # sess = Session(app)

    db.init_app(app)
    with app.app_context():
        # Initialize models
        from .models import Usage, ComputerStatus, Player, User
        # from . import gsheet_autowriter
        db.create_all()

        # Initialize apscheduler
        apscheduler.init_app(app)
        apscheduler.start()

        # Initialize JWT
        jwt.init_app(app)

        # Import parts of our application
        from application.openrec import openrec_bp
        from application.auth import auth_bp
        from application.models_routes import models_bp
        from application.react_route import react_bp

        # Register Blueprints
        app.register_blueprint(openrec_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(models_bp)
        app.register_blueprint(react_bp)

        return app
