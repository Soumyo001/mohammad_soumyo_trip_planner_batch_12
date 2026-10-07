from app.data.constants import TripStatus, TRIP_REQUIRED_FIELDS
from app.models.trip import Trip
from app.services.traveler import count_trip_travelers
from app.utils.error_util import NotFoundError, ConflictError
from app.utils.extension_util import db
from app.utils.validation_util import (
    require_fields,
    parse_string,
    parse_date,
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

def capacity_fits_current_travelers(trip, max_travelers):
    traveler_count = count_trip_travelers(trip)
    if max_travelers < traveler_count:
        raise ConflictError(
            f"max travelers cannot be reduced below the current traveler count {traveler_count}",
            error_code="CAPACITY_BELOW_TRAVELER_COUNT"
        )

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
    capacity_fits_current_travelers(trip, max_travelers)

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