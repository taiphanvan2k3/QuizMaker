from ..utils.firestore_utils import initialize_firestore
from datetime import datetime, timedelta

db = initialize_firestore()
section_class_ref = db.collection("section_class")


def create_user_if_not_exist(user_info):
    user_ref = db.collection("users").document(user_info["id"])
    user = user_ref.get()
    if not user.exists:
        user_ref.set(
            {
                "email": user_info["email"],
                "display_name": (
                    f"{user_info['family_name']} {user_info['given_name']}"
                    if "family_name" in user_info
                    else user_info["given_name"]
                ),
                "picture": user_info["picture"],
                "auth_provider": "google",
            }
        )

def save_access_token(user_id, access_token, expires_in):
    access_token_ref = db.collection("access_tokens").document()
    access_token_ref.set(
        {
            "user_id": user_id,
            "access_token": access_token,
            "expires_at": datetime.now() + timedelta(seconds=expires_in),
        }
    )