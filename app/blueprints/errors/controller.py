from . import errors_bp, env
from ..utils.helpers import render_template_util


@errors_bp.route("/not-found")
def not_found():
    return render_template_util(env, "not_found.html", title="Error page")


@errors_bp.route("/server-error/<string:message>")
def server_error(message):
    return render_template_util(
        env, "server_error.html", title="Error page", message=message
    )


@errors_bp.route("/coming-soon")
def coming_soon():
    return render_template_util(env, "coming_soon.html", title="Coming soon")