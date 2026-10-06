from flask import Blueprint, jsonify
from app.services import trip as trip_service
from app.utils.validation_util import get_json_body

trip_bp = Blueprint("trips", __name__)

@trip_bp.post("/trips")
def create_trip():
    body = get_json_body()
    trip = trip_service.create_trip(body)
    return jsonify(trip.to_json()), 201

@trip_bp.get("/trips")
def list_trips():
    trips = trip_service.list_trips()
    return jsonify([trip.to_json() for trip in trips]), 200

@trip_bp.get("/trips/<int:trip_id>")
def get_trip(trip_id):
    trip = trip_service.get_trip(trip_id)
    return jsonify(trip.to_json()), 200

@trip_bp.put("/trips/<int:trip_id>")
def update_trip(trip_id):
    trip = trip_service.get_trip(trip_id)
    update_body = get_json_body()
    updated_trip = trip_service.update_trip(trip, update_body)
    return jsonify(updated_trip.to_json()), 200

@trip_bp.delete("/trips/<int:trip_id>")
def delete_trip(trip_id):
    trip = trip_service.get_trip(trip_id)
    trip_service.delete_trip(trip)
    return jsonify({"message": f"Trip {trip_id} deleted successfully."}), 200
