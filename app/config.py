from app.constants import Paths

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + Paths.DATABASE_PATH
    SQLALCHEMY_TRACK_MODIFICATIONS = False