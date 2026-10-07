import os

EMAIL_REGEX = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
MONEY_PRECISION = 2

DEFAULT_ERROR_CODES = {
    400: "BAD_REQUEST",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    415: "UNSUPPORTED_MEDIA_TYPE",
    500: "INTERNAL_SERVER_ERROR",
}

TRIP_REQUIRED_FIELDS = (
    "destination",
    "start_date",
    "end_date",
    "budget",
    "max_travelers",
)

TRAVELER_REQUIRED_FIELDS = (
    "name",
    "email",
)

EXPENSE_REQUIRED_FIELDS = (
    "title",
    "amount",
)

STATUS_REQUIRED_FIELDS = (
    "status",
)

class Paths:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    DATABASE_PATH = os.path.join(INSTANCE_DIR, "trip_planner.db")
    ENV_FILE = os.path.join(BASE_DIR, ".env")

class TripStatus:
    PLANNED = "PLANNED"
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ALL = (
        PLANNED,
        ONGOING,
        COMPLETED,
        CANCELLED,
    )
    TERMINAL = (
        COMPLETED,
        CANCELLED,
    )
    ALLOWED_TRANSITIONS = {
        PLANNED: (ONGOING, CANCELLED),
        ONGOING: (COMPLETED, CANCELLED),
        COMPLETED: (),
        CANCELLED: ()
    }