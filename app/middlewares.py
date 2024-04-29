from flask import request, g
from functools import wraps
from firebase_admin import firestore
from .blueprints.utils.firestore_utils import initialize_firestore

# Initialize Firestore DB
db = initialize_firestore()


# Middleware to fetch user information
def fetch_user_info_middleware():
    # Check if the request is not for static files
    if not request.endpoint or request.endpoint.startswith("static"):
        return

    access_token = request.cookies.get("access_token")

    # Fetch user information from Firestore based on user_id
    if access_token:
        access_token_ref = (
            db.collection("access_tokens")
            .where("access_token", "==", access_token)
            .order_by("expires_at", direction=firestore.Query.DESCENDING)
            .limit(1)
        )

        access_token_ref = access_token_ref.get()
        if len(access_token_ref) > 0:
            user_id = access_token_ref[0].to_dict()["user_id"]
            user_ref = db.collection("users").document(user_id)
            user = user_ref.get()
            if user.exists:
                g.user_info = user.to_dict()
    else:
        # Handle case where user_id is not provided
        g.user_info = None
