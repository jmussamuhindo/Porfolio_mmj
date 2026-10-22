"""Application factory for the portfolio site."""
from flask import Flask

from .config import Config
from .routes import main_bp


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(main_bp)

    # Make the current year available in every template (footer).
    @app.context_processor
    def inject_globals():
        from datetime import date
        return {"current_year": date.today().year}

    return app
