from . import auth_bp, env, oauth, url_for
from . import model
from ..utils.helpers import render_template_util
from flask import redirect, session, make_response, request, g
import json


# Route cho trang chủ
@auth_bp.route("/register")
def register():
    section_classes = model.get_all_section_classes()
    return render_template_util(
        env, "register.html", section_classes=section_classes, title="Đây là trang chủ"
    )


@auth_bp.route("/login")
def login():
    temp = g.user_info
    # Lưu URL trước đó vào session
    session["previous_url"] = "/" if request.referrer is None else request.referrer
    if "user_info" in session and "user_info" in request.cookies:
        return redirect(session.pop("previous_url", "/"))
    return render_template_util(env, "login.html", title="Đăng nhập")


@auth_bp.route("/signin-google")
def google_login():
    google = oauth.create_client("google")
    redirect_uri = url_for("auth.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()

    # Lưu thông tin user vào Firestore
    model.create_user_if_not_exist(user_info)
    model.save_access_token(user_info["id"], token["access_token"], token["expires_in"])

    # Lưu thông tin user vào session và cookie
    user_info_str = json.dumps(user_info)
    session["user_info"] = user_info_str
    response = make_response(redirect("/"))

    response.set_cookie("user_info", user_info_str, max_age=3600)
    response.set_cookie("access_token", token["access_token"], max_age=3600, httponly=True)
    return response


@auth_bp.route("/logout")
def logout():
    response = make_response(redirect("/"))
    response.delete_cookie("user_info", path="/")
    return response
