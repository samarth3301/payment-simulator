from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error="Bad Request", message=str(e)), 400

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"Server Error: {e}")
        return jsonify(error="Internal Server Error"), 500