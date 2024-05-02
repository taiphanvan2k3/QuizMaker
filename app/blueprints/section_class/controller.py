from . import section_class_bp, env
from . import model
from ..utils.helpers import render_template_util
from ...middlewares import login_required
from flask import request, jsonify


@section_class_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    * Author: Phan Van Tai, created at: 28/04/2024\n
    * Description: This function will render the section class list page or serve for searching 
    section classes by their types
    """
    if request.method == "GET":
        section_type = request.args.get("sectionType", "all")
        return render_template_util(
            env,
            "index.html",
            title="Danh sách học phần",
            sections=model.get_all_section_classes(section_type),
            sectionType=section_type,
        )
    elif request.method == "POST":
        response_info = {}
        try:
            sections = model.get_all_section_classes(request.form["sectionType"])
            partial_content = render_template_util(
                env,
                "partials/_sectionsList.html",
                sections=sections,
            )

            response_info = {
                "code": 200,
                "html": partial_content,
            }
        except Exception as e:
            response_info = {
                "code": 500,
                "message": str(e),
            }
        return jsonify(response_info)


@section_class_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_set():
    """
    * Author: Phan Van Tai, created at: 28/04/2024
    * Description: This function show a UI to create a new section class or update an existing one
    """
    if request.method == "GET":
        return render_template_util(
            env,
            "create.html",
            title="Tạo học phần mới",
        )
