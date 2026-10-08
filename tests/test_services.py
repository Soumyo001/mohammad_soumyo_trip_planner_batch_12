from types import SimpleNamespace
import pytest
from app.services import expense, traveler, trip
from app.utils.error_util import ConflictError


def test_capacity_below_travelers(monkeypatch):
    t = SimpleNamespace(id=1)
    monkeypatch.setattr(trip, "count_trip_travelers", lambda _: 4)

    with pytest.raises(ConflictError) as error:
        trip.ensure_capacity_fits_current_travelers(t, 3)

    assert error.value.error_code == "CAPACITY_BELOW_TRAVELER_COUNT"


@pytest.mark.parametrize("status", ["COMPLETED", "CANCELLED"])
def test_cannot_edit_a_finished_trip(status):
    t = SimpleNamespace(status=status)

    with pytest.raises(ConflictError) as error:
        trip.ensure_trip_is_editable(t)

    assert error.value.error_code == "TRIP_NOT_EDITABLE"


def test_traveler_cannot_join_overlapping_trips(monkeypatch):
    t = SimpleNamespace(id=1)
    person = SimpleNamespace(id=5, email="karim@gmail.com")
    overlapping_trip = SimpleNamespace(id=9)

    monkeypatch.setattr(
        traveler,
        "find_overlapping_trip",
        lambda t, p: overlapping_trip,
    )

    with pytest.raises(ConflictError) as error:
        traveler.ensure_no_overlapping_trip(t, person)

    assert error.value.error_code == "OVERLAPPING_TRIP"


def test_cannot_add_an_expense_to_a_cancelled_trip():
    t = SimpleNamespace(status="CANCELLED")

    with pytest.raises(ConflictError) as error:
        expense.ensure_trip_accepts_expenses(t)

    assert error.value.error_code == "TRIP_NOT_ACCEPTING_EXPENSES"

def test_trip_full(monkeypatch):
    t = SimpleNamespace(id=1, max_travelers=5)
    monkeypatch.setattr(traveler, "count_trip_travelers", lambda t: 5)

    with pytest.raises(ConflictError) as error:
        traveler.ensure_trip_has_free_seat(t)

    assert error.value.error_code == "TRIP_FULL"

def test_expense_can_use_the_exact_remaining_budget(monkeypatch):
    t = SimpleNamespace(id=1)
    monkeypatch.setattr(expense, "remaining_trip_budget", lambda t: 2500.50)
    expense.ensure_expense_fits_budget(t, 2500.50)