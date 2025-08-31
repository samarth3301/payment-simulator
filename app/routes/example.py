from flask import Blueprint

example_bp = Blueprint('example', __name__)


@example_bp.route("/", methods=['POST'])
async def example_route():
    return {"message": "This is an example route."}, 200