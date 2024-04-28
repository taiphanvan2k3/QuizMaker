from firebase_admin import credentials, firestore, initialize_app, get_app

def initialize_firestore():
    try:
        # Kiểm tra xem ứng dụng Firebase đã được khởi tạo chưa
        get_app()
    except Exception as e:
        # Nếu chưa, khởi tạo nó
        cred = credentials.Certificate("key.json")
        initialize_app(cred)
        print("Initialize: Firebase app has been initialized.")
    return firestore.client()