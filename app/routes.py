from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api/v1")

@health_bp.get("/health")
def health_check():
    return jsonify({"status": "ok"}), 200