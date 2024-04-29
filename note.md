1. Khi tạo ra 1 blueprint, ta đã tạo cho nó một tên. Do đó có thể dùng tên đó, kết hợp với tên của hàm để tạo ra một URL
khi dùng url_for, ví dụ:
```python
url_for('auth.login')
```
thì sẽ trả về URL của hàm login trong blueprint auth.

2. Khi tải fontawesome thì lưu ý cần bỏ thư mục webfonts vào static folder và thay đổi lại nếu url trong file all.min.css
để có thể link đến được thư mục webfonts trong static folder. 

3. Các hàm, đối tượng như url_for, g muốn dùng trong template thì cần đăng ký nó vào biến global của biến env
```python
env.globals["url_for"] = url_for
env.globals["g"] = g
```

4. session trong flask là 1 đối tượng, nó sẽ dùng cookie được configure để lưu trữ thông tin của session. Khi cookie này bị xoá
thì sẽ mất session, vì lúc request lên server, server không tìm thấy cookie nào dùng để lưu trữ session nên sẽ tạo ra 1 session mới.
Và session sẽ mất khi ta tắt trình duyệt hoặc xoá cookie.
Configure tại đây:
```python
app.config["SESSION_COOKIE_NAME"] = "session_id"
```

5. Có thể định nghĩa các filter (decorator) trước mỗi action của controller, ví dụ:
```python
def login_required(view):
    """
    Middleware to check if the user is logged in or not
    Author: Phan Van Tai, created at: 29/04/2024
    """

    # Dùng wraps để đảm bảo giữ lại thông tin metadata của hàm gốc khi bạn đóng gói một hàm trong một decorator khác.
    # Khi bạn không sử dụng @wraps, các thuộc tính của hàm gốc có thể bị mất đi và được thay thế bởi các thuộc tính của hàm được bọc
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user_info is None:
            return redirect(url_for(login_endpoint))
        return view(*args, **kwargs)

    return wrapped_view
```
Sau đó sử dụng nó như sau:
```python
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")
```

Hoặc viết filter khác như:
```python
def permission_required(permission):
    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            # Kiểm tra quyền truy cập của người dùng ở đây, sử dụng biến g.user_info hoặc bất kỳ cơ chế xác thực nào bạn sử dụng
            if not check_permission(g.user_info, permission):
                # Nếu không có quyền, chuyển hướng đến trang cấp quyền hoặc trang lỗi
                return redirect(url_for("auth.permission_denied"))
            return view(*args, **kwargs)
        return wrapped_view
    return decorator
```
lúc dùng: 
```python
@app.route("/admin")
@permission_required("admin")
def admin():
    return render_template("admin.html")
```    