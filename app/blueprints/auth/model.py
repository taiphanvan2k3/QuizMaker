from ..utils.firestore_utils import initialize_firestore
from datetime import datetime, timedelta
from ..utils.algoliasearch import save_to_algolia
import threading

db = initialize_firestore()
section_class_ref = db.collection("section_class")


def create_user_if_not_exist(user_info):
    user_ref = db.collection("users").document(user_info["id"])
    user = user_ref.get()
    if not user.exists:
        display_name = (
            f"{user_info['family_name']} {user_info['given_name']}"
            if "family_name" in user_info
            else user_info["given_name"]
        )

        user_ref.set(
            {
                "email": user_info["email"],
                "display_name": display_name,
                "picture": user_info["picture"],
                "auth_provider": "google",
            }
        )

        # Lưu vào algolia search, tạo thread để làm điều này
        data = {
            "objectID": user_info["id"],
            "email": user_info["email"],
            "display_name": display_name,
            "picture": user_info["picture"],
        }
        threading.Thread(target=save_to_algolia, args=("users", data)).start()


def save_access_token(user_id, access_token, expires_in):
    access_token_ref = db.collection("access_tokens").document()
    access_token_ref.set(
        {
            "user_id": user_id,
            "access_token": access_token,
            "expires_at": datetime.now() + timedelta(seconds=expires_in),
        }
    )


def get_firebase_configure():
    return (
        db.collection("client_api_key").document("FP8dR7vhdNGhzzhVmVTd").get().to_dict()
    )
