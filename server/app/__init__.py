from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from server.extensions import db
from server.config import DevelopmentConfig
from server.app.routes.get_routes import get_routes_blueprint
from server.app.routes.post_routes import post_routes_blueprint
from server.app.routes.put_routes import put_routes_blueprint
from server.app.routes.delete_routes import delete_routes_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    cors = CORS(app, origins ='*')

    # Register Blueprints (routes)
    # app.register_blueprint(routes_blueprint)
    # app.register_blueprint(example_blueprint)
    # app.register_blueprint(main_blueprint)


    # Register Blueprints
    app.register_blueprint(get_routes_blueprint)
    app.register_blueprint(post_routes_blueprint)
    app.register_blueprint(put_routes_blueprint)
    app.register_blueprint(delete_routes_blueprint)

    return app
