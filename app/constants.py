import os

DEFAULT_ERROR_CODES = {
    400: "BAD_REQUEST",
    401: "UNAUTHORIZED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    415: "UNSUPPORTED_MEDIA_TYPE",
    429: "TOO_MANY_REQUESTS",
    500: "INTERNAL_SERVER_ERROR",
}

class Paths:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    DATABASE_PATH = os.path.join(INSTANCE_DIR, "trip_planner.db")