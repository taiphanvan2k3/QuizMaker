from . import section_class_bp, env
from . import model
from ..utils.helpers import render_template_util, create_thread_and_run
from ..utils.algoliasearch import autocomplete
from ..utils.openai import get_definition_gpt
from ...middlewares import login_required
from flask import request, jsonify, redirect, url_for, g
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate


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
            active_menu="section_class",
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
    * Description: This function is used for showing UI for creating a new section class
    """
    try:
        if request.method == "GET":
            return render_template_util(
                env,
                "create-edit.html",
                title="Tạo học phần mới",
                active_menu="section_class",
            )
        else:
            data = request.get_json()
            section_class_name = data["sectionClassName"]
            if section_class_name is None or section_class_name == "":
                return jsonify(
                    {"code": 400, "message": "Tên học phần không được để trống"}
                )

            model.create_section_class(
                SectionClassCreateUpdate(
                    section_class_name=section_class_name,
                    section_class_desc=data["sectionClassDesc"],
                    vocabularies=data["vocabularies"],
                    is_public=data["isPublic"],
                )
            )
            return jsonify({"code": 200})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit(id):
    """
    * Author: Phan Van Tai, created at: 14/05/2024
    * Description: This function is used for viewing and editing a section class
    """
    if request.method == "GET":
        try:
            section_class_data = model.get_section_class_by_id(id)
            return render_template_util(
                env,
                "create-edit.html",
                title="Chỉnh sửa lớp học phần",
                section_class_data=section_class_data,
            )
        except Exception as e:
            return redirect(url_for("errors.not_found", message=str(e)))
    else:
        try:
            data = request.get_json()
            section_class_name = data["sectionClassName"]
            if section_class_name is None or section_class_name == "":
                return jsonify(
                    {"code": 400, "message": "Tên học phần không được để trống"}
                )

            model.update_section_class(
                SectionClassCreateUpdate(
                    data["id"],
                    section_class_name,
                    data["sectionClassDesc"],
                    data["vocabularies"],
                    data["isPublic"],
                )
            )

            return jsonify({"code": 200})
        except Exception as e:
            return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("<id>", methods=["GET"])
@login_required
def section_class_detail(id):
    """
    * Author: Phan Van Tai, created at: 11/05/2024
    * Description: View the detail of a section class
    """
    section_class = model.get_section_class_by_id(id)

    # Lấy notification_id từ request
    notification_id = request.args.get("notification_id")
    if notification_id:
        current_user = g.user_info
        create_thread_and_run(
            model.update_notification_status, (current_user["id"], notification_id)
        )

    if section_class is None:
        return redirect(url_for("errors.not_found"))
    return render_template_util(
        env,
        "detail.html",
        title=f"Học phần: {section_class.name}",
        section_class=section_class,
        active_menu="section_class",
    )


@section_class_bp.route("/autocomplete_en", methods=["GET"])
@login_required
def autocomplete_en():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Auto complete search for English words with prefix matching.
    """
    try:
        query = request.args.get("query", "")
        results = autocomplete(query)
        return jsonify({"code": 200, "data": [hit["word"] for hit in results["hits"]]})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("/autocomplete_vi", methods=["GET"])
@login_required
def autocomplete_vi():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Auto complete search for English words with prefix matching.
    """
    try:
        query = request.args.get("query", "")
        results = autocomplete(query)
        return jsonify({"code": 200, "data": [results["hits"][0]["translation"]]})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("/get-definition", methods=["GET"])
def get_definition_route():
    """
    * Author: Tran Dinh Manh, created at: 11/05/2024
    * Description: Get definition of a word from GPT.
    """
    try:
        word = request.args.get("word")
        definition = get_definition_gpt(word)
        return jsonify({"code": 200, "data": definition})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})

@section_class_bp.route("exam/check/<id>", methods=["GET"])
@login_required
def check_section_class_exam(id):
    """
    * Author: Tran Dinh Manh, created at: 23/05/2024
    * Description: Check if the section class has enough vocabularies to create an exam.
    """
    section_class = model.get_section_class_by_id(id)
    if section_class is None:
        return jsonify({"error": "Không tìm thấy lớp học."}), 404
    if len(section_class.vocabularies) < 4:
        return jsonify({"error": "Không thể tạo bài kiểm tra. Số lượng từ vựng ít hơn 4."}), 400
    return jsonify({"success": True, "redirect_url": url_for('section_class.section_class_exam', id=id)}), 200

@section_class_bp.route("exam/<id>", methods=["GET"])
@login_required
def section_class_exam(id):
    """
    * Author: Tran Dinh Manh, created at: 13/05/2024
    * Description: Redirect to exam page of a section class.
    """
    section_class = model.get_section_class_by_id(id)
    if section_class is None:
        return redirect(url_for("errors.not_found"))
    quizs = model.create_quiz(section_class.vocabularies)
    return render_template_util(
        env,
        "exam.html",
        title=f"Học phần: {section_class.name}",
        title_exam=f"Kiểm tra từ vựng: {section_class.name}",
        quizs=quizs,
        active_menu="section_class",
    )


# Các action liên quan đến members
@section_class_bp.route("<id>/members", methods=["GET"])
@login_required
def get_all_members(id):
    """
    * Author: Phan Van Tai, created at: 16/05/2024
    * Description: Get all members are in a section class
    """
    try:
        return jsonify({"code": 200, "data": model.get_all_members(id)})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("<id>/share-to-user", methods=["POST"])
@login_required
def share_to_user(id):
    """
    * Author: Phan Van Tai, created at: 16/05/2024
    * Description: Add a new member to a section class (save to pending members)
    """
    try:
        data = request.form
        model.share_to_user(id, data["email"])
        return jsonify({"code": 200})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})


@section_class_bp.route("<id>/response-invitation", methods=["POST"])
@login_required
def response_invitation(id):
    """
    * Author: Phan Van Tai, created at: 18/05/2024
    * Description: Response to an invitation to join a section class
    """
    try:
        is_accept = request.form["status"]
        model.response_invitation(id, is_accept)
        return jsonify({"code": 200})
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})
