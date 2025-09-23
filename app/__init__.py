from flask import Flask
from app.routes import register_routes
from app.errors.handlers import register_error_handlers
from app.utils.logger import init_logger
from app.config.database import init_db
from flask_migrate import upgrade
from flask_cors import CORS

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.envVars.Config")

    # Enable CORS for all routes
    CORS(app)

    # Initialize database
    init_db(app)

    # Auto-upgrade database migrations on app start
    with app.app_context():
        upgrade()

    register_routes(app)
    register_error_handlers(app)
    init_logger(app)

    return app