# src/middleware/error_handler.py

from flask import jsonify
from src.utils.logger import get_logger

logger = get_logger(__name__)


def register_error_handlers(app):
    
    @app.errorhandler(400)
    def bad_request(error):
        logger.error(f"Bad request: {error}")
        return jsonify({"error": "Bad request", "message": str(error)}), 400
    
    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"Not found: {error}")
        return jsonify({"error": "Resource not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return jsonify({"error": "An unexpected error occurred"}), 500