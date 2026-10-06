from flask import Blueprint
from app.routes.health import health_bp

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)