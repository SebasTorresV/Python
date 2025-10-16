import os
from datetime import datetime

from flask import Flask
from dotenv import load_dotenv

from .extensions import db, migrate


def create_app(test_config: dict | None = None) -> Flask:
    """Application factory for the Chivospot project."""
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    default_db_path = os.path.join(app.instance_path, "chivospot.sqlite")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL")
        or f"sqlite:///{default_db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models  # noqa: F401  # register models with SQLAlchemy

    from .routes.main import main_bp

    app.register_blueprint(main_bp)

    @app.context_processor
    def inject_current_year():
        return {
            "current_year": datetime.now().year
        }

    return app
