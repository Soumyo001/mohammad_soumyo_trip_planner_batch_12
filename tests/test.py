import pytest
from types import SimpleNamespace

from app.services import trip, traveler, expense
from app.utils.error_util import ConflictError


def test_capacity_below_current_travelers(monkeypatch):
    t = SimpleNamespace(id=1)

    monkeypatch.setattr(trip, "count_trip_travelers", lambda t: 4)

    with pytest.raises(ConflictError) as error:
        trip.ensure_capacity_fits_current_travelers(t, 3)

    assert error.value.error_code == "CAPACITY_BELOW_TRAVELER_COUNT"


@pytest.mark.parametrize("status", ["COMPLETED", "CANCELLED"])
def test_finished_trip_cannot_be_edited(status):
    t = SimpleNamespace(status=status)

    with pytest.raises(ConflictError) as error:
        trip.ensure_trip_is_editable(t)

    assert error.value.error_code == "TRIP_NOT_EDITABLE"


def test_overlapping_trip(monkeypatch):
    t = SimpleNamespace(id=1)
    person = SimpleNamespace(id=5, email="karim@gmail.com")
    other_trip = SimpleNamespace(id=9)

    monkeypatch.setattr(traveler, "find_overlapping_trip", lambda t, p: other_trip)

    with pytest.raises(ConflictError) as error:
        traveler.ensure_no_overlapping_trip(t, person)

    assert error.value.error_code == "OVERLAPPING_TRIP"


def test_expense_not_allowed_on_cancelled_trip():
    t = SimpleNamespace(status="CANCELLED")

    with pytest.raises(ConflictError) as error:
        expense.ensure_trip_accepts_expenses(t)

    assert error.value.error_code == "TRIP_NOT_ACCEPTING_EXPENSES"


def test_expense_equal_to_remaining_budget_is_ok(monkeypatch):
    t = SimpleNamespace(id=1)
    monkeypatch.setattr(expense, "remaining_trip_budget", lambda t: 2500.50)
    expense.ensure_expense_fits_budget(t, 2500.50)