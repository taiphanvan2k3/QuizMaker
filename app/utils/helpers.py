from flask import render_template_string

def render_template_util(env, template_name, **kwargs):
    template = env.get_template(template_name)
    return render_template_string(template.render(**kwargs))