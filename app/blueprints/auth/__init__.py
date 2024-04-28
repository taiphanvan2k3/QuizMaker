from flask import  url_for
from ..utils import helpers
from ...extensions import oauth

auth_bp = helpers.create_blueprint("auth", __name__)

# Tạo biến env để load template từ các thư mục khác nhau
env = helpers.create_environment(__file__)
env.globals["url_for"] = url_for

# Import các route từ controller
from . import controller