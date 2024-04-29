from . import auth_bp, env, oauth
from . import model
from ..utils.helpers import render_template_util
from flask import redirect, make_response, g, url_for, session


# Route cho trang chủ
@auth_bp.route("/register")
def register():
    section_classes = model.get_all_section_classes()
    return render_template_util(
        env, "register.html", section_classes=section_classes, title="Đây là trang chủ"
    )


@auth_bp.route("/login")
def login():
    current_user = g.user_info
    if current_user:
        return redirect(session.get("redirected_from", "/"))
    return render_template_util(env, "login.html", title="Đăng nhập")


@auth_bp.route("/signin-google")
def google_login():
    google = oauth.create_client("google")
    redirect_uri = url_for("auth.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()

    # Lưu thông tin user vào Firestore
    model.create_user_if_not_exist(user_info)

    # Lưu thông tin user vào session và cookie
    response = make_response(redirect("/"))
    response.set_cookie("user_id", user_info["id"], max_age=3600, path="/", httponly=True)
    return response


@auth_bp.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("user_id", path="/")
    return response
