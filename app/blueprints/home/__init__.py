from flask import url_for
from ..utils import helpers
home_bp = helpers.create_blueprint("home", __name__)

# Tạo biến env để load template từ các thư mục khác nhau
env = helpers.create_environment(__file__)

# Đăng ký hàm url_for vào global để có thể sử dụng trong template
env.globals["url_for"] = url_for

# Import các route từ controller
from . import controller