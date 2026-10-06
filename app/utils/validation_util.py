from datetime import date
from flask import request
from app.utils.error_util import ValidationError

def get_json_body():
    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        raise ValidationError("Request body must be a valid JSON object")
    return body

def require_fields(body, field_names):
    missing_fields = [field_name for field_name in field_names if field_name not in body]
    if missing_fields:
        missing_fields_str = ", ".join(missing_fields)
        raise ValidationError(f"Missing required fields: {missing_fields_str}.")

def parse_string(value, field_name):
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field_name}' must be a non-empty string")
    return value.strip()

def parse_date(value, field_name):
    if not isinstance(value, str):
        raise ValidationError(f"'{field_name}' must be a date string in YYYY-MM-DD format")

    try:
        return date.fromisoformat(value)
    except ValueError:
        raise ValidationError(f"'{field_name}' must be a valid date in YYYY-MM-DD format")

def parse_positive_number(value, field_name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"'{field_name}' must be a number")
    if value <= 0:
        raise ValidationError(f"'{field_name}' must be greater than zero")
    return float(value)

def parse_positive_integer(value, field_name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"'{field_name}' must be an integer")
    if value <= 0:
        raise ValidationError(f"'{field_name}' must be greater than zero")
    return value

def validate_date_order(start_date, end_date):
    if end_date <= start_date:
        raise ValidationError(
            "'end_date' must be later than 'start_date'",
            error_code="INVALID_DATE_RANGE"
        )