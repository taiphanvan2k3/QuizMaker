from flask import Flask, render_template, g
from datetime import timedelta
from .extensions import oauth  # Import OAuth object từ file extensions.py
from .middlewares import fetch_user_info_middleware, cookie_renewal
import os
from dotenv import load_dotenv

load_dotenv()

# Đăng ký các Blueprint
from .blueprints.auth import auth_bp
from .blueprints.section_class import section_class_bp
from .blueprints.home import home_bp
from .blueprints.errors import errors_bp
from .blueprints.vocabularies import vocabularies_bp
from .blueprints.users import users_bp


def create_app():
    app = Flask(__name__)

    # Đăng kí middleware
    app.before_request(fetch_user_info_middleware)
    app.after_request(cookie_renewal)

    app.secret_key = os.getenv("APP_SECRET_KEY")
    app.config["SESSION_COOKIE_NAME"] = "session_id"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

    oauth.init_app(app)

    oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        access_token_url="https://accounts.google.com/o/oauth2/token",
        access_token_params=None,
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        authorize_params=None,
        api_base_url="https://www.googleapis.com/oauth2/v1/",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        client_kwargs={"scope": "email profile"},
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    )

    # Thêm Blueprint vào app
    register_blueprint(app)

    app.jinja_env.auto_reload = True
    app.config["FLASK_APP"] = "app.py"
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    return app


def register_blueprint(app: Flask):
    app.register_blueprint(home_bp, url_prefix="/")
    app.register_blueprint(auth_bp)
    app.register_blueprint(section_class_bp, url_prefix="/section_class")
    app.register_blueprint(errors_bp, url_prefix="/errors")
    app.register_blueprint(vocabularies_bp, url_prefix="/vocabularies")
    app.register_blueprint(users_bp, url_prefix="/users")
