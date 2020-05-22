from flask import make_response, jsonify


class Serializer:
    """This class serializes data."""

    @classmethod
    def serialize(cls, response, status_code, message):
        """Serializes data output."""
        if status_code in (400, 401, 403, 404, 405, 500):
            return make_response(jsonify({
                "status": status_code,
                "message": message,
                "error": response
            }), status_code)
        return make_response(jsonify({
            "status": status_code,
            "message": message,
            "data": response
        }), status_code)
