from . import auth_bp, env, oauth
from . import model
from ..utils.helpers import render_template_util
from flask import redirect, make_response, g, url_for, session, jsonify


# Route cho trang chủ
@auth_bp.route("/register")
def register():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Show register page
    """
    section_classes = model.get_all_section_classes()
    return render_template_util(
        env, "register.html", section_classes=section_classes, title="Đây là trang chủ"
    )


@auth_bp.route("/login")
def login():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Show login page
    """
    current_user = g.user_info
    if current_user:
        # Nếu user đã đăng nhập thì chuyển hướng về trang trước đó
        return redirect(session.get("redirected_from", "/"))
    return render_template_util(env, "login.html", title="Đăng nhập")


@auth_bp.route("/signin-google")
def google_login():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Redirect user to Google OAuth2 login page
    """
    google = oauth.create_client("google")
    redirect_uri = url_for("auth.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@auth_bp.route("/authorize")
def authorize():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Authorize user with Google OAuth2
    """
    google = oauth.create_client("google")
    google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()

    # Lưu thông tin user vào Firestore
    model.create_user_if_not_exist(user_info)

    # Lưu thông tin user vào session và cookie
    response = make_response(redirect("/"))
    response.set_cookie(
        "user_id", user_info["id"], max_age=12 * 3600, path="/", httponly=True
    )
    return response


@auth_bp.route("/logout")
def logout():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Log out user by deleting user_id cookie
    """
    response = make_response(redirect("/"))
    response.delete_cookie("user_id", path="/")
    response.delete_cookie("session_id", path="/")
    return response


@auth_bp.route("/firebase-configure", methods=["POST"])
def get_firebase_configure():
    """
    * Author: Phan Van Tai, created at: 17/05/2024
    * Description: Get firebase configure
    """
    try:
        firebase_configure = model.get_firebase_configure()
        return jsonify({"data": firebase_configure}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
