from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config.from_object('config.Config')

    db.init_app(app)
    jwt.init_app(app)

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
