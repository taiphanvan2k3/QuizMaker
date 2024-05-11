from ..utils.firestore_utils import initialize_firestore
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate
from .entities.SectionClassDto import SectionClassDto
from flask import g
from datetime import datetime
import pytz

db = initialize_firestore()
section_class_ref = db.collection("section_class")
timezone = pytz.timezone("Asia/Ho_Chi_Minh")


def get_all_section_classes(section_type="all"):
    current_user = g.user_info
    query = section_class_ref
    if section_type != "all":
        # Các lớp học phần tự tạo
        query = query.where("owner_email", "==", current_user["email"])
    else:
        # Hiển thị tất cả học phần mà user tham gia
        query = query.where("members", "array_contains", current_user["email"])
    query = query.order_by("created_at", direction="DESCENDING")

    # Dùng stream() thay vì get() để giúp nhận dữ liệu một cách tuần tự thay vì
    # nhận toàn bộ dữ liệu một lúc khi dùng get()
    sections = query.stream()

    section_classes_groupby = {}
    for section in sections:
        section_data = section.to_dict()
        owner = section_data["owner"].get()
        if owner.exists:
            owner = owner.to_dict()

        # Group các section class theo cùng 1 tháng
        date_str = f"Tháng {section_data['created_at'].month} năm {section_data['created_at'].year}"
        current_section_class = SectionClassDto(
            section.id,
            section_data["name"],
            owner["display_name"],
            owner["picture"],
            section_data["vocab_count"],
        )

        if date_str not in section_classes_groupby:
            section_classes_groupby[date_str] = [current_section_class]
        else:
            section_classes_groupby[date_str].append(current_section_class)

    return section_classes_groupby


def create_section_class(section_class: SectionClassCreateUpdate):
    current_user = g.user_info

    user_ref = db.collection("users").document(current_user["id"])
    new_section_class_ref = section_class_ref.add(
        {
            "name": section_class.section_class_name,
            "description": section_class.section_class_desc,
            "owner": user_ref,  # Lưu một reference đến user tạo ra lớp học phần
            "owner_email": current_user["email"],
            "members": [current_user["email"]],
            "created_at": datetime.now(timezone),
            "vocab_count": len(section_class.vocabularies),
        }
    )

    # Tạo 1 sub-collection vocabularies cho lớp học phần mới
    # Do new_section_class_ref chứa 2 phần tử (DateTime, DocumentReference)
    sub_collection = new_section_class_ref[1].collection("vocabularies")
    for idx, vocab in enumerate(section_class.vocabularies):
        sub_collection.add(
            {
                "english": vocab["english_text"],
                "vietnamese": vocab["vietnamese_text"],
                "order": idx + 1,
            }
        )
