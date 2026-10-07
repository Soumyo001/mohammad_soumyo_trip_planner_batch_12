from app.data.constants import TripStatus, TRAVELER_REQUIRED_FIELDS
from app.models.traveler import Traveler
from app.models.trip import Trip
from app.models.trip_traveler import TripTraveler
from app.utils.error_util import ConflictError, NotFoundError
from app.utils.extension_util import db
from app.utils.validation_util import require_fields, parse_string, parse_email

def count_trip_travelers(trip):
    return db.session.scalar(
        db.select(db.func.count())
        .select_from(TripTraveler)
        .where(TripTraveler.trip_id == trip.id)
    )

def find_traveler_by_email(email):
    return db.session.scalars(
        db.select(Traveler).where(Traveler.email == email)
    ).first()

def get_traveler(traveler_id):
    traveler = db.session.get(Traveler, traveler_id)
    if traveler is None:
        raise NotFoundError(
            f"Traveler {traveler_id} not found",
            error_code="TRAVELER_NOT_FOUND"
        )
    return traveler

def get_participation(trip, traveler):
    return db.session.scalars(
        db.select(TripTraveler).where(
            TripTraveler.trip_id == trip.id,
            TripTraveler.traveler_id == traveler.id
        )
    ).first()

def find_overlapping_trip(trip, traveler):
    return db.session.scalars(
        db.select(Trip)
        .join(TripTraveler, TripTraveler.trip_id == Trip.id)
        .where(
            TripTraveler.traveler_id == traveler.id,
            Trip.id != trip.id,
            Trip.start_date <= trip.end_date,
            Trip.end_date >= trip.start_date
        )
    ).first()

def ensure_trip_accepts_travelers(trip):
    if trip.status != TripStatus.PLANNED:
        raise ConflictError(
            f"Travelers can only be added while the trip status is PLANNED. This trip is {trip.status}",
            error_code="TRIP_NOT_PLANNED"
        )

def ensure_trip_allows_traveler_removal(trip):
    if trip.status in TripStatus.TERMINAL:
        raise ConflictError(
            f"A {trip.status} trip cannot be modified",
            error_code="TRIP_NOT_EDITABLE"
        )

def ensure_traveler_not_in_this_trip(trip, traveler):
    if get_participation(trip, traveler) is not None:
        raise ConflictError(
            f"Traveler {traveler.email} is already a part of this trip",
            error_code="DUPLICATE_TRAVELER"
        )

def ensure_trip_has_free_seat(trip):
    if count_trip_travelers(trip) >= trip.max_travelers:
        raise ConflictError(
            "The trip is full and cannot accept anymore travelers",
            error_code="TRIP_FULL"
        )

def ensure_no_overlapping_trip(trip, traveler):
    overlapping_trip = find_overlapping_trip(trip, traveler)
    if overlapping_trip is not None:
        raise ConflictError(
            f"Traveler {traveler.email} is already in trip {overlapping_trip.id} which overlaps this trip: {trip.id}",
            error_code="OVERLAPPING_TRIP"
        )

def get_or_create_traveler(name, email):
    traveler = find_traveler_by_email(email)
    if traveler is not None:
        return traveler

    traveler = Traveler(name=name, email=email)
    db.session.add(traveler)
    db.session.flush()
    return traveler

def add_traveler(trip, body):
    ensure_trip_accepts_travelers(trip)
    require_fields(body, TRAVELER_REQUIRED_FIELDS)

    name = parse_string(body["name"], "name")
    email = parse_email(body["email"], "email")

    traveler = get_or_create_traveler(name, email)

    ensure_traveler_not_in_this_trip(trip, traveler)
    ensure_trip_has_free_seat(trip)
    ensure_no_overlapping_trip(trip, traveler)

    participation = TripTraveler(trip_id=trip.id, traveler_id=traveler.id)
    db.session.add(participation)
    db.session.commit()
    return traveler

def remove_traveler(trip, traveler_id):
    ensure_trip_allows_traveler_removal(trip)

    traveler = get_traveler(traveler_id)
    participation = get_participation(trip, traveler)
    if participation is None:
        raise NotFoundError(
            f"Traveler {traveler_id} is not a part of this trip {trip.id}",
            error_code="TRAVELER_NOT_IN_TRIP"
        )
    db.session.delete(participation)
    db.session.commit()