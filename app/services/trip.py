from app.data.constants import TripStatus, TRIP_REQUIRED_FIELDS, MONEY_PRECISION, STATUS_REQUIRED_FIELDS
from app.models.trip import Trip
from app.services.traveler import count_trip_travelers
from app.services.expense import total_trip_expense
from app.utils.error_util import NotFoundError, ConflictError
from app.utils.extension_util import db
from app.utils.validation_util import (
    require_fields,
    parse_string,
    parse_date,
    parse_status,
    parse_positive_number,
    parse_positive_integer,
    validate_date_order
)

def get_trip(trip_id):
    trip = db.session.get(Trip, trip_id)
    if trip is None:
        raise NotFoundError(
            f"Trip {trip_id} was not found",
            error_code="TRIP_NOT_FOUND"
        )
    return trip

def list_trips():
    return db.session.scalars(db.select(Trip).order_by(Trip.id)).all()

def get_trip_summary(trip):
    traveler_count = count_trip_travelers(trip)
    total_expense = total_trip_expense(trip)

    return {
        "trip_id": trip.id,
        "destination": trip.destination,
        "status": trip.status,
        "budget": trip.budget,
        "max_travelers": trip.max_travelers,
        "traveler_count": traveler_count,
        "available_seats": trip.max_travelers - traveler_count,
        "total_expense": total_expense,
        "remaining_budget": round(trip.budget - total_expense, MONEY_PRECISION)
    }

def ensure_capacity_fits_current_travelers(trip, max_travelers_cap):
    traveler_count = count_trip_travelers(trip)
    if max_travelers_cap < traveler_count:
        raise ConflictError(
            f"max travelers capacity cannot be reduced below current traveler count {traveler_count}",
            error_code="CAPACITY_BELOW_TRAVELER_COUNT"
        )

def ensure_trip_is_editable(trip):
    if trip.status in TripStatus.TERMINAL:
        raise ConflictError(
            f"A {trip.status} trip cannot be edited",
            error_code="TRIP_NOT_EDITABLE"
        )

def ensure_transition_is_allowed(trip, new_status):
    if new_status not in TripStatus.ALLOWED_TRANSITIONS[trip.status]:
        raise ConflictError(
            f"A trip cannot be moved from {trip.status} to {new_status}",
            error_code="INVALID_STATUS_TRANSITION"
        )

def update_trip_status(trip, body):
    require_fields(body, STATUS_REQUIRED_FIELDS)
    new_status = parse_status(body["status"], "status")
    ensure_transition_is_allowed(trip, new_status)
    trip.status = new_status
    db.session.commit()
    return trip

def create_trip(body):
    require_fields(body, TRIP_REQUIRED_FIELDS)

    destination = parse_string(body["destination"], "destination")
    start_date = parse_date(body["start_date"], "start_date")
    end_date = parse_date(body["end_date"], "end_date")
    budget = parse_positive_number(body["budget"], "budget")
    max_travelers = parse_positive_integer(body["max_travelers"], "max_travelers")

    validate_date_order(start_date, end_date)

    trip = Trip(
        destination=destination,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        max_travelers=max_travelers,
        status=TripStatus.PLANNED
    )
    db.session.add(trip)
    db.session.commit()
    return trip

def update_trip(trip, body):
    ensure_trip_is_editable(trip)

    destination = trip.destination
    start_date = trip.start_date
    end_date = trip.end_date
    budget = trip.budget
    max_travelers = trip.max_travelers

    if "destination" in body:
        destination = parse_string(body["destination"], "destination")
    if "start_date" in body:
        start_date = parse_date(body["start_date"], "start_date")
    if "end_date" in body:
        end_date = parse_date(body["end_date"], "end_date")
    if "budget" in body:
        budget = parse_positive_number(body["budget"], "budget")
    if "max_travelers" in body:
        max_travelers = parse_positive_integer(body["max_travelers"], "max_travelers")

    validate_date_order(start_date, end_date)
    ensure_capacity_fits_current_travelers(trip, max_travelers)

    trip.destination = destination
    trip.start_date = start_date
    trip.end_date = end_date
    trip.budget = budget
    trip.max_travelers = max_travelers

    db.session.commit()
    return trip

def delete_trip(trip):
    db.session.delete(trip)
    db.session.commit()