from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
cors = CORS()
jwt = JWTManager()

def init_extensions(app):
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)