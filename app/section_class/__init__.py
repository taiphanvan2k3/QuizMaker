from flask import Blueprint
from jinja2 import FileSystemLoader, Environment
import os

section_class_bp = Blueprint("section_class", __name__, template_folder="templates")

# Tạo biến env để load template từ các thư mục khác nhau
env = Environment(
    loader=FileSystemLoader(
        [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "section_class", "templates"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shared", "templates"),
        ]
    )
)

# Import các route từ views.py
from . import controller
