from . import home_bp, env
from . import model
from ..utils.helpers import render_template_util
from ..section_class.model import get_recent_section_classes

@home_bp.route("/")
def index():
    recent_section_classes = get_recent_section_classes()
    return render_template_util(
        env, "index.html", title="Home", active_menu="home", recent_section_classes=recent_section_classes
    )