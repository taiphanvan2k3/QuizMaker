from . import section_class_bp, env
from . import model
from ..utils.helpers import render_template_util

@section_class_bp.route("/")
def index():
    return render_template_util(
        env, "index.html", title="Học phần của bạn"
    )