from app.data.constants import TripStatus, EXPENSE_REQUIRED_FIELDS, MONEY_PRECISION
from app.models.expense import Expense
from app.utils.error_util import ConflictError
from app.utils.extension_util import db
from app.utils.validation_util import require_fields, parse_string, parse_positive_number

def total_trip_expense(trip):
    total = db.session.scalar(
        db.select(db.func.coalesce(db.func.sum(Expense.amount), 0.0))
        .where(Expense.trip_id == trip.id)
    )
    return round(total, MONEY_PRECISION)

def remaining_trip_budget(trip):
    return round(trip.budget - total_trip_expense(trip), MONEY_PRECISION)

def ensure_trip_accepts_expenses(trip):
    if trip.status not in (TripStatus.PLANNED, TripStatus.ONGOING):
        raise ConflictError(
            f"Expenses can only be added while the trip status is PLANNED or ONGOING. This trip is {trip.status}",
            error_code="TRIP_NOT_ACCEPTING_EXPENSES"
        )

def ensure_expense_fits_budget(trip, expense_amount):
    remaining_budget = remaining_trip_budget(trip)
    if round(expense_amount, MONEY_PRECISION) > remaining_budget:
        raise ConflictError(
            f"The expense amount {expense_amount} exceeds the remaining budget of {remaining_budget}",
            error_code="BUDGET_EXCEEDED"
        )

def add_expense(trip, body):
    ensure_trip_accepts_expenses(trip)
    require_fields(body, EXPENSE_REQUIRED_FIELDS)

    title = parse_string(body["title"], "title")
    amount = parse_positive_number(body["amount"], "amount")

    ensure_expense_fits_budget(trip, amount)

    expense = Expense(trip_id=trip.id, title=title, amount=amount)
    db.session.add(expense)
    db.session.commit()
    return expense