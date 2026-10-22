"""Configuration. Override values with environment variables when deploying."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DATA_DIR = BASE_DIR / "data"
    DEBUG = os.environ.get("FLASK_DEBUG", "0") == "1"
