from app import create_app

app = create_app()
if __name__ == "__main__":
    # Thêm debug=True để Flask tự reload khi có thay đổi
    app.run(debug=True)