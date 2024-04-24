from flask import Blueprint
from jinja2 import FileSystemLoader, Environment
import os


home_bp = Blueprint("home", __name__, template_folder="templates")

# Tạo biến env để load template từ các thư mục khác nhau
env = Environment(
    loader=FileSystemLoader(
        [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "home", "templates"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared", "templates"),
        ]
    )
)

# Import các route từ views.py
from . import controller