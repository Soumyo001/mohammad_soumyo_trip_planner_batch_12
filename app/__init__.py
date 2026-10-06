import os
from app.config.config import Config
from app.data.constants import Paths
from app.utils.error_util import register_error_handlers
from app.routes import register_blueprints
from app.utils.extension_util import db
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(Paths.INSTANCE_DIR, exist_ok=True)

    db.init_app(app)
    register_error_handlers(app)
    register_blueprints(app)

    with app.app_context():
        from app import models
        db.create_all()

    return app