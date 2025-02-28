from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from server.extensions import db
from server.config import DevelopmentConfig
from server.app.example_blueprint import example_blueprint
from server.app.main_blueprint import main_blueprint
from server.app.routes_blueprint import routes_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    cors = CORS(app, origins ='*')

    # Register Blueprints (routes)
    app.register_blueprint(routes_blueprint)
    app.register_blueprint(example_blueprint)
    app.register_blueprint(main_blueprint)

    return app
