from types import SimpleNamespace
import pytest
from app.services import expense, traveler, trip
from app.utils.error_util import ConflictError


def test_trip_capacity_cannot_be_less_than_current_traveler_count(monkeypatch):
    current_trip = SimpleNamespace(id=1)
    monkeypatch.setattr(trip, "count_trip_travelers", lambda _: 4)

    with pytest.raises(ConflictError) as ex_info:
        trip.ensure_capacity_fits_current_travelers(current_trip, 3)

    assert ex_info.value.error_code == "CAPACITY_BELOW_TRAVELER_COUNT"


@pytest.mark.parametrize("status", ["COMPLETED", "CANCELLED"])
def test_cannot_edit_a_finished_trip(status):
    current_trip = SimpleNamespace(status=status)

    with pytest.raises(ConflictError) as ex_info:
        trip.ensure_trip_is_editable(current_trip)

    assert ex_info.value.error_code == "TRIP_NOT_EDITABLE"


def test_traveler_cannot_join_overlapping_trips(monkeypatch):
    current_trip = SimpleNamespace(id=1)
    person = SimpleNamespace(id=5, email="karim@gmail.com")
    overlapping_trip = SimpleNamespace(id=9)

    monkeypatch.setattr(
        traveler,
        "find_overlapping_trip",
        lambda _trip, _person: overlapping_trip,
    )

    with pytest.raises(ConflictError) as ex_info:
        traveler.ensure_no_overlapping_trip(current_trip, person)

    assert ex_info.value.error_code == "OVERLAPPING_TRIP"


def test_cannot_add_an_expense_to_a_cancelled_trip():
    cancelled_trip = SimpleNamespace(status="CANCELLED")

    with pytest.raises(ConflictError) as ex_info:
        expense.ensure_trip_accepts_expenses(cancelled_trip)

    assert ex_info.value.error_code == "TRIP_NOT_ACCEPTING_EXPENSES"

def test_trip_full(monkeypatch):
    current_trip = SimpleNamespace(id=1, max_travelers=5)
    monkeypatch.setattr(traveler, "count_trip_travelers", lambda t: 5)

    with pytest.raises(ConflictError) as ex_info:
        traveler.ensure_trip_has_free_seat(current_trip)

    assert ex_info.value.error_code == "TRIP_FULL"

def test_expense_can_use_the_exact_remaining_budget(monkeypatch):
    current_trip = SimpleNamespace(id=1)
    monkeypatch.setattr(expense, "remaining_trip_budget", lambda _: 2500.50)
    expense.ensure_expense_fits_budget(current_trip, 2500.50)