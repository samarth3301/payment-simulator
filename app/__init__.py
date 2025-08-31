from flask import Flask
from app.routes import register_routes
from app.errors.handlers import register_error_handlers
from app.utils.logger import init_logger
from app.config.database import init_db

def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("app.config.envVars.Config")

    # Initialize database
    init_db(app)

    register_routes(app)
    register_error_handlers(app)
    init_logger(app)

    return app