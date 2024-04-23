from flask import render_template
from . import auth_bp

# Route cho trang chủ
@auth_bp.route('/')
def home():
    return render_template('home.html')

@auth_bp.route('/login')
def login():
    return render_template('login.html')