from flask import request, g, session, redirect, url_for
from .blueprints.utils.firestore_utils import initialize_firestore
from functools import wraps

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

    if request.endpoint.startswith("auth") and request.endpoint != login_endpoint:
        return

    if request.endpoint != login_endpoint:
        session["redirected_from"] = request.url

    user_id = request.cookies.get("user_id")
    if user_id:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        if user:
            g.user_info = user.to_dict()
        else:
            g.user_info = None
    else:
        g.user_info = None


def login_required(view):
    """
    Middleware to check if the user is logged in or not
    Author: Phan Van Tai, created at: 29/04/2024
    """

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user_info is None:
            return redirect(url_for(login_endpoint))
        return view(*args, **kwargs)

    return wrapped_view
