from . import users_bp
from flask import request, jsonify
from ..utils.algoliasearch import get_user_by_query


@users_bp.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("query", "")
        results = get_user_by_query(query)
        return jsonify({"code": 200, "data": results})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})
