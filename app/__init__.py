import os
from config import Config
from constants import Paths
from errors import register_error_handlers
from extensions import db
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(Paths.INSTANCE_DIR, exist_ok=True)

    db.init_app(app)
    register_error_handlers(app)

    from routes import health_bp, api_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    return app