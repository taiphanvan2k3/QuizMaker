from flask import render_template_string, url_for, g
import threading
import os


def render_template_util(env, template_name, **kwargs):
    template = env.get_template(template_name)
    return render_template_string(template.render(**kwargs))


def create_blueprint(blueprint_name, import_name, template_folder="templates"):
    from flask import Blueprint

    return Blueprint(blueprint_name, import_name, template_folder=template_folder)


def create_environment(file_path):
    from jinja2 import FileSystemLoader, Environment
    import os

    env = Environment(
        # Load template từ các thư mục khác nhau, dùng os.path.abspath(file_path) để tính đường dẫn
        # từ vị trí của file_path truyền vào
        loader=FileSystemLoader(
            [
                os.path.join(os.path.dirname(os.path.abspath(file_path)), "templates"),
                os.path.join(
                    os.path.dirname(os.path.abspath(file_path)), "..", "..", "layouts"
                ),
            ]
        )
    )
    env.globals["url_for"] = url_for
    env.globals["g"] = g
    return env


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_time_diff(start, end):
    time_diff = end - start
    if time_diff.days == 0:
        hours = time_diff.seconds // 3600
        if hours == 0:
            minutes = time_diff.seconds // 60
            if minutes == 0:
                time_diff = "vài giây trước"
            else:
                time_diff = f"{minutes} phút trước"
        else:
            time_diff = f"{hours} giờ trước"
    elif time_diff.days <= 31:
        time_diff = f"{time_diff.days} ngày trước"
    elif time_diff.days <= 365:
        time_diff = f"{time_diff.days // 30} tháng trước"
    else:
        time_diff.days = f"{time_diff.days // 365} năm trước"
    return time_diff


def create_thread_and_run(func, args):
    thread = threading.Thread(target=func, args=args)
    thread.start()
    return thread
