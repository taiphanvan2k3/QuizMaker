from ..utils import helpers

users_bp = helpers.create_blueprint("users", __name__)

# Tạo biến env để load template từ các thư mục khác nhau
env = helpers.create_environment(__file__)

# Import các route từ controller
from . import controller
