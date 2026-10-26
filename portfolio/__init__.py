"""Application factory for the portfolio site."""
from flask import Flask

from .config import Config
from .routes import main_bp


def create_app(config_class=Config, **overrides) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.update(overrides)

    app.register_blueprint(main_bp)

    # Private admin panel: only when running locally, never in the static build.
    admin_enabled = bool(app.config.get("ADMIN_ENABLED"))
    if admin_enabled:
        from .admin import admin_bp
        app.register_blueprint(admin_bp)

    # Make the current year available in every template (footer).
    @app.context_processor
    def inject_globals():
        from datetime import date
        return {"current_year": date.today().year,
                "admin_enabled": admin_enabled}

    return app
