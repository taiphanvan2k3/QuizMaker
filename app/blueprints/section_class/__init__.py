from ..utils import helpers
section_class_bp = helpers.create_blueprint("section_class", __name__)

# Tạo biến env để load template từ các thư mục khác nhau
env = helpers.create_environment(__file__)

# Import các route từ controller
from . import controller