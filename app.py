from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
import models
import os

# Blueprints
from resources.course_item import blp as CourseItemBlueprint
from resources.specialization import blp as SpecializationBlueprint
from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    app = Flask(__name__)

    # Swagger & API config
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Specialization REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/"

    # Database config
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL",
        "sqlite:///data.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT config
    app.config["JWT_SECRET_KEY"] = "tasnim123"  

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)

    api = Api(app)

    # Register blueprints
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CourseItemBlueprint)
    api.register_blueprint(SpecializationBlueprint)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
