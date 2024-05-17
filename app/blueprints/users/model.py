from ..utils.firestore_utils import initialize_firestore
from flask import g, json, current_app as app

db = initialize_firestore()
users_collection_ref = db.collection("users")


def generate(collection_watch):
    for change in collection_watch:
        yield "data: {}\n\n".format(json.dumps(change))


def snapshot_callback(snapshot, changes, read_time):
    for change in changes:
        data = {
            "type": change.type,
            "data": change.document.to_dict(),
        }
        print(f"Document {change.document.id} has been {change.type}.")
        yield data


def on_receive_notifications():
    with app.app_context():
        # Lấy sub-collection UserNotifications bên trong collections Notifications
        current_user = g.current_user
        notifications_ref = (
            db.collection("users_notifications")
            .document(current_user["uid"])
            .collection("notifications")
        )

        # Lắng nghe sự thay đổi trong subcollection
        notifications_ref.on_snapshot(snapshot_callback)
        return notifications_ref
