from flask import Flask
# Đăng ký các Blueprint
from .auth import auth_bp
from .section_class import section_class_bp
from .home import home_bp

def create_app():
    app = Flask(__name__)

    # Thêm Blueprint vào app
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(section_class_bp, url_prefix='/section_class')

    app.jinja_env.auto_reload = True
    app.config["FLASK_APP"] = "app.py"
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return app