from . import section_class_bp, env
from . import model
from ..utils.helpers import render_template_util
from ...middlewares import login_required
from flask import request, jsonify, redirect, url_for
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate
from algoliasearch.search_client import SearchClient

client = SearchClient.create("KI4POLGT5H", "dfb2ba6c58d39ccb0a7b576db6ff2d32")
algolia_index = client.init_index("vocab_en_vi_3000_freq")
settings = {"searchableAttributes": ["word", "translation"]}
algolia_index.set_settings(settings)


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
    try:
        if request.method == "GET":
            return render_template_util(
                env,
                "create.html",
                title="Tạo học phần mới",
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


@section_class_bp.route("<id>", methods=["GET"])
@login_required
def section_class_detail(id):
    """
    * Author: Phan Van Tai, created at: 11/05/2024
    * Description: View the detail of a section class
    """
    section_class = model.get_section_class_by_id(id)
    if section_class is None:
        return redirect(url_for("errors.not_found"))
    return render_template_util(
        env,
        "detail.html",
        title=f"Học phần: {section_class.name}",
        section_class=section_class,
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
        results = algolia_index.search(
            query,
            {
                "attributesToRetrieve": ["word", "translation"],
                "hitsPerPage": 5,
                "restrictSearchableAttributes": ["word"],
            },
        )
        return jsonify({"code": 200, "data": [hit["word"] for hit in results["hits"]]})
    except Exception as e:
        print("error: ", e)
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
        results = algolia_index.search(
            query,
            {
                "attributesToRetrieve": ["word", "translation"],
                "hitsPerPage": 5,
                "restrictSearchableAttributes": ["word"],
            },
        )
        return jsonify(
            {"code": 200, "data": [hit["translation"] for hit in results["hits"]]}
        )
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)})
