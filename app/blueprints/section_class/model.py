from ..utils.firestore_utils import initialize_firestore
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate
from .entities.SectionClassDto import SectionClassDto
from flask import g
from datetime import datetime
import pytz, time

db = initialize_firestore()
section_class_ref = db.collection("section_class")
timezone = pytz.timezone("Asia/Ho_Chi_Minh")


def get_all_section_classes(section_type="all") -> list[SectionClassDto]:
    current_user = g.user_info
    query = section_class_ref
    if section_type != "all":  # các lớp học phần tự tạo
        query = query.where("created_by.email", "==", current_user["email"])

    # Chỉ hiển thị các lớp học phần mà user này có tham gia
    query = query.where("members", "array_contains", current_user["email"])

    # Dùng stream() thay vì get() để giúp nhận dữ liệu một cách tuần tự thay vì
    # nhận toàn bộ dữ liệu một lúc khi dùng get()
    sections = query.stream()

    section_classes = []
    for section in sections:
        section_data = section.to_dict()
        owner = section_data["owner"].get()
        if owner.exists:
            owner = owner.to_dict()
        section_classes.append(
            SectionClassDto(
                section.id,
                section_data["name"],
                owner["display_name"],
                owner["picture"],
                section_data["created_at"],
            )
        )

        # Truy cập sub-collection vocabularies
        vocabularies = section.reference.collection("vocabularies").get()
        section_classes[-1].vocab_count = len(list(vocabularies))

    if section_type != "all":
        section_classes = [section_classes[0]]
    return section_classes


def create_section_class(section_class: SectionClassCreateUpdate):
    current_user = g.user_info

    user_ref = db.collection("users").document(current_user["id"])
    new_section_class_ref = section_class_ref.add(
        {
            "name": section_class.section_class_name,
            "description": section_class.section_class_desc,
            "owner": user_ref,
            "members": [current_user["email"]],
            "created_at": datetime.now(timezone),
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

    # Delay 3s
    time.sleep(3)
