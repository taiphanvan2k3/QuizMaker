from . import auth_bp, env
from . import model
from ..utils.helpers import render_template_util


# Route cho trang chủ
@auth_bp.route("/register")
def register():
    section_classes = model.get_all_section_classes()
    return render_template_util(
        env, "register.html", section_classes=section_classes, title="Đây là trang chủ"
    )


@auth_bp.route("/login")
def login():
    return render_template_util(
        env, "login.html", title="Đây là trang chủ :)))"
    )
