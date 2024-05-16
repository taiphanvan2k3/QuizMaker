from ..utils.firestore_utils import initialize_firestore

db = initialize_firestore()
users_collection_ref = db.collection("users")

def get_users_by_query(query):
    users_ref = users_collection_ref.where("display_name", "contains", query)
        