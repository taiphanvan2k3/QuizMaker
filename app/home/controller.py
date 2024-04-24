from . import home_bp, env
from . import model
from ..utils.helpers import render_template_util

@home_bp.route("/")
def index():
    return render_template_util(
        env, "index.html", title="Home"
    )