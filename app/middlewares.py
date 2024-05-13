from flask import request, g, session, redirect, url_for
from .blueprints.utils.firestore_utils import initialize_firestore
from functools import wraps
import datetime, pytz

db = initialize_firestore()
login_endpoint = "auth.login"


def fetch_user_info_middleware():
    """
    Middleware to fetch user info from Firestore before each request
    Author: Phan Van Tai, created at: 29/04/2024
    """
    # Check if the request is not for static files
    if not request.endpoint or request.endpoint.startswith("static"):
        return

    # Một số endpoint không cần phải kiểm tra user info
    if request.endpoint.startswith("auth") and request.endpoint != login_endpoint:
        return

    if request.endpoint != login_endpoint:
        session["redirected_from"] = request.url

    user_id = request.cookies.get(
        "user_id", session["user_id"] if "user_id" in session else None
    )
    if user_id:
        # Cập nhật lại cookie để giữ user_id luôn tồn tại
        session["user_id"] = user_id

        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        if user:
            g.user_info = {"id": user.id, **user.to_dict()}
        else:
            g.user_info = None
    else:
        g.user_info = None


def login_required(view):
    """
    Middleware to check if the user is logged in or not
    Author: Phan Van Tai, created at: 29/04/2024
    """

    # Dùng wraps để đảm bảo giữ lại thông tin metadata của hàm gốc khi bạn đóng gói một hàm trong một decorator khác.
    # Khi bạn không sử dụng @wraps, các thuộc tính của hàm gốc có thể bị mất đi và được thay thế bởi các thuộc tính của hàm được bọc
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user_info is None:
            return redirect(url_for(login_endpoint))
        return view(*args, **kwargs)

    return wrapped_view


def cookie_renewal(response):
    """
    Middleware to renew user_id cookie
    """
    # Check if the request is not for static files
    if not request.endpoint or request.endpoint.startswith("static"):
        return response

    # Cập nhật lại cookie user_id
    if "user_id" in session:
        expire_time = datetime.datetime.now(
            pytz.timezone("Asia/Ho_Chi_Minh")
        ) + datetime.timedelta(hours=12)
        response.set_cookie("user_id", session["user_id"], expires=expire_time)
    return response
