from flask import Flask
from flask_migrate import Migrate
from server.extensions import init_extensions, db
from server.config import DevelopmentConfig
from server.app.routes.get_routes import get_routes_blueprint
from server.app.routes.post_routes import post_routes_blueprint
from server.app.routes.put_routes import put_routes_blueprint
from server.app.routes.delete_routes import delete_routes_blueprint
from server.app.routes.auth_routes import auth_routes_blueprint
from server.app.routes.user_routes import user_routes_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Initialize extensions (DB, CORS, etc.)
    init_extensions(app)

    # Initialize migration
    migrate = Migrate(app, db)

    # Register Blueprints
    app.register_blueprint(get_routes_blueprint)
    app.register_blueprint(post_routes_blueprint)
    app.register_blueprint(put_routes_blueprint)
    app.register_blueprint(delete_routes_blueprint)
    app.register_blueprint(auth_routes_blueprint, url_prefix="/auth")
    app.register_blueprint(user_routes_blueprint, url_prefix="/users")

    return app
