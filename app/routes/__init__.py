from flask import Blueprint
from app.routes.health import health_bp
from app.routes.trip import trip_bp
from app.routes.traveler import traveler_bp
from app.routes.expense import expense_bp

api_bp = Blueprint("api", __name__, url_prefix="/api/v1")
api_bp.register_blueprint(trip_bp)
api_bp.register_blueprint(traveler_bp)
api_bp.register_blueprint(expense_bp)

def register_blueprints(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp)