from . import vocabularies_bp, env
from ..utils.helpers import render_template_util
from flask import request, jsonify
from .entities.VocabularyCreateUpdate import VocabularyCreateUpdate
from .model import update_vocabulary


@vocabularies_bp.route("/update/<string:id>", methods=["POST"])
def update(id):
    try:
        form = request.form
        update_vocabulary(
            VocabularyCreateUpdate(
                form.get("sectionClassId"),
                id,
                form.get("english"),
                form.get("vietnamese"),
                form.get("isStared"),
            )
        )
        return jsonify({"message": "Vocabulary updated", "code": 200})
    except Exception as e:
        return jsonify({"message": str(e)}), 400
