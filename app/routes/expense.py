from flask import Blueprint, jsonify
from app.services import expense as expense_service
from app.services import trip as trip_service
from app.utils.validation_util import get_json_body

expense_bp = Blueprint("expenses", __name__)

@expense_bp.post("/trips/<int:trip_id>/expenses")
def add_expense(trip_id):
    trip = trip_service.get_trip(trip_id)
    body = get_json_body()
    expense = expense_service.add_expense(trip, body)
    return jsonify(expense.to_json()), 201