1. Khi tạo ra 1 blueprint, ta đã tạo cho nó một tên. Do đó có thể dùng tên đó, kết hợp với tên của hàm để tạo ra một URL
khi dùng url_for, ví dụ:
```python
url_for('auth.login')
```
thì sẽ trả về URL của hàm login trong blueprint auth.

2. Khi tải fontawesome thì lưu ý cần bỏ thư mục webfonts vào static folder và thay đổi lại nếu url trong file all.min.css
để có thể link đến được thư mục webfonts trong static folder. 