import os
from app.data.constants import Paths
from dotenv import load_dotenv

load_dotenv(Paths.ENV_FILE)

DEFAULT_DATABASE_URI = "sqlite:///" + Paths.DATABASE_PATH

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or DEFAULT_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HOST = os.environ.get("FLASK_HOST", "127.0.0.1")
    PORT = int(os.environ.get("FLASK_PORT", "5000"))
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "t")