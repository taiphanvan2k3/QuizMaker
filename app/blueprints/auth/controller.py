from . import auth_bp, env, oauth
from . import model
from ..utils.helpers import render_template_util
from flask import redirect, url_for, session, make_response, jsonify
from urllib.parse import urlencode
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
    if 'profile' in session:
        email = dict(session)['profile']['email']
    else:
        email = "Guest"
    return render_template_util(
        env, "login.html", title=f'You are logge in as {email}!'
    )

@auth_bp.route("/signin-google")
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    user_info_json = json.dumps(user_info)
    response = make_response(redirect('/'))
    response.set_cookie('user_info', user_info_json, max_age=3600)

    return response

@auth_bp.route('/logout')
def logout():
    response = make_response(redirect('/'))
    response.delete_cookie('user_info', path='/')
    return response