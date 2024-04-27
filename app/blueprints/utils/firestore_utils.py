from firebase_admin import credentials, firestore, initialize_app

def initialize_firestore():
    # Đọc file config và khởi tạo đối tượng Firestore
    # Note: Do chạy file app.py nên đường dẫn sẽ tính từ thư mục chứa file app.py và file key.json cùng cấp
    # nên ta chỉ cần truyền tên file key.json là đủ
    cred = credentials.Certificate("key.json")
    initialize_app(cred)
    return firestore.client()