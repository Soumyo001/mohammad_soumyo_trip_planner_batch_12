from flask import jsonify
from werkzeug.exceptions import HTTPException
from constants import DEFAULT_ERROR_CODES

class ApiResponseError(Exception):
    error_code = "BAD_REQUEST"
    status_code = 400
    
    def __init__(self, message, error_code=None, status_code=None):
        super().__init__(message)
        self.message = message
        if error_code is not None:
            self.error_code = error_code
        if status_code is not None:
            self.status_code = status_code

    def to_json(self):
        return {
            "error": self.error_code,
            "message": self.message
        }

class ValidationError(ApiResponseError):
    error_code = "VALIDATION_ERROR"
    status_code = 400

class NotFoundError(ApiResponseError):
    error_code = "NOT_FOUND"
    status_code = 404

class ConflictError(ApiResponseError):
    error_code = "CONFLICT"
    status_code = 409

def register_error_handlers(app):
    @app.errorhandler(ApiResponseError)
    def handle_api_response_error(error):
        return jsonify(error.to_json()), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        body = {
            "error": DEFAULT_ERROR_CODES.get(error.code, "ERROR"),
            "message": error.description
        }
        return jsonify(body), error.code

    @app.errorhandler(Exception)
    def handle_general_exceptions(error):
        app.logger.exception("unhandled exception")
        body = {
            "error": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occured"
        }
        return jsonify(body), 500
        