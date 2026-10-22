"""Entry point. Local dev:  python app.py   |  Production:  gunicorn app:app"""
import os

from portfolio import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=app.config["DEBUG"])
