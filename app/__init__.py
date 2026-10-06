import os
from app.config import Config
from app.constants import Paths
from app.errors import register_error_handlers
from app.extensions import db
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(Paths.INSTANCE_DIR, exist_ok=True)

    db.init_app(app)
    register_error_handlers(app)

    from app.routes import health_bp, api_bp
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        from app.models import Trip
        db.create_all()

    return app