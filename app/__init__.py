from flask import Flask

def create_app():
    app = Flask(__name__)

    # Đăng ký các Blueprint
    from .auth import auth_bp

    # Thêm Blueprint vào app
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    app.jinja_env.auto_reload = True
    app.config["FLASK_APP"] = "app.py"
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    return app