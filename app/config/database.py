from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask

# Global database instance
db = SQLAlchemy()
migrate = Migrate()

def init_db(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)