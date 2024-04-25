from flask import render_template_string

def render_template_util(env, template_name, **kwargs):
    template = env.get_template(template_name)
    return render_template_string(template.render(**kwargs))

def create_blueprint(blueprint_name, import_name, template_folder="templates"):
    from flask import Blueprint
    return Blueprint(blueprint_name, import_name, template_folder=template_folder)

def create_environment(file_path):
    from jinja2 import FileSystemLoader, Environment
    import os

    return Environment(
        loader=FileSystemLoader(
            [
                os.path.join(os.path.dirname(os.path.abspath(file_path)), "templates"),
                os.path.join(os.path.dirname(os.path.abspath(file_path)), "..", "shared", "templates"),
            ]
        )
    )