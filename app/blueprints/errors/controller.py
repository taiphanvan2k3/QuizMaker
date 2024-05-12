from . import errors_bp, env
from ..utils.helpers import render_template_util


@errors_bp.route("/not-found")
def not_found():
    return render_template_util(env, "not_found.html", title="Error page")
