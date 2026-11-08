from flask import Flask

from app.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    """Build and configure a Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
