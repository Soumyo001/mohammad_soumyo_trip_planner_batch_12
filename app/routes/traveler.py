from flask import jsonify, Blueprint
from app.services import trip as trip_service
from app.services import traveler as traveler_service
from app.utils.validation_util import get_json_body

traveler_bp = Blueprint("travelers", __name__)

@traveler_bp.post("/trips/<int:trip_id>/travelers")
def add_traveler(trip_id):
    trip = trip_service.get_trip(trip_id)
    body = get_json_body()
    traveler = traveler_service.add_traveler(trip, body)
    return jsonify(traveler.to_json()), 201

@traveler_bp.delete("/trips/<int:trip_id>/travelers/<int:traveler_id>")
def remove_traveler(trip_id, traveler_id):
    trip = trip_service.get_trip(trip_id)
    traveler_service.remove_traveler(trip, traveler_id)
    return jsonify({
        "message": f"Traveler {traveler_id} has been removed from trip {trip_id}"
    }), 200