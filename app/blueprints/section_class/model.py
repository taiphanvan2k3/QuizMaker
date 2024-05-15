from ..utils.firestore_utils import initialize_firestore
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate
from .entities.SectionClassDto import SectionClassDto
from .entities.SectionClassDetailDto import SectionClassDetailDto
from flask import g
from datetime import datetime
import pytz
import random
from ..utils.openai import get_definition_gpt

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
            "is_public": section_class.is_public,
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
                "english": vocab["english_text"].strip(),
                "vietnamese": vocab["vietnamese_text"].strip(),
                "order": idx + 1,
            }
        )


def update_section_class(section_class: SectionClassCreateUpdate):
    edited_section_class_ref = section_class_ref.document(section_class.id)
    edited_section_class_ref.update(
        {
            "name": section_class.section_class_name,
            "description": section_class.section_class_desc,
            "is_public": section_class.is_public,
            "vocab_count": len(section_class.vocabularies),
        }
    )

    # Thay đổi danh sách vocabulary của lớp học phần
    vocabularies_ref = edited_section_class_ref.collection("vocabularies")

    # Chỉ thay đổi các vocabulary đã thay đổi
    current_vocabularies = vocabularies_ref.stream()
    current_vocabularies_data = {
        vocab.id: vocab.to_dict() for vocab in current_vocabularies
    }
    new_vocabularies = {vocab["id"]: vocab for vocab in section_class.vocabularies}

    for vocab_id, vocab_data in new_vocabularies.items():
        vocab_data = {
            "english": vocab_data["english_text"],
            "vietnamese": vocab_data["vietnamese_text"],
            "order": vocab_data["order"],
        }

        if vocab_id in current_vocabularies_data:
            vocabularies_ref.document(vocab_id).update(vocab_data)
        else:
            vocabularies_ref.add(vocab_data)

    # Xóa các vocabulary không còn tồn tại
    deleted_vocab_ids = set(current_vocabularies_data.keys()) - set(
        new_vocabularies.keys()
    )

    if len(deleted_vocab_ids) > 0:
        for vocab_id in deleted_vocab_ids:
            vocabularies_ref.document(vocab_id).delete()


def get_section_class_by_id(section_class_id: str):
    section_class_doc = section_class_ref.document(section_class_id).get(
        ["name", "description", "created_at", "is_public"]
    )
    if not section_class_doc.exists:
        return None

    # Lấy danh sách vocabulary của lớp học phần
    vocabularies_ref = (
        section_class_doc.reference.collection("vocabularies")
        .order_by("order", direction="ASCENDING")
        .stream()
    )

    vocabularies = []
    for vocab in vocabularies_ref:
        vocab_data = vocab.to_dict()
        vocabularies.append({"id": vocab.id, **vocab_data})

    current_user = g.user_info
    created_at = section_class_doc.get("created_at")

    # Tìm độ chênh lệch về thời gian hiện tại với created_at
    time_diff = datetime.now(timezone) - created_at
    if time_diff.days <= 31:
        time_diff = f"{time_diff.days} ngày trước"
    elif time_diff.days <= 365:
        time_diff = f"{time_diff.days // 30} tháng trước"
    else:
        time_diff.days = f"{time_diff.days // 365} năm trước"

    return SectionClassDetailDto(
        section_class_id,
        section_class_doc.get("name"),
        section_class_doc.get("description"),
        owner={
            "display_name": current_user["display_name"],
            "picture": current_user["picture"],
        },
        created_at={"actual": created_at, "simple": time_diff},
        vocabularies=vocabularies,
        is_public=section_class_doc.get("is_public"),
    )

def create_quiz(vocabularies):
    quiz = []
    all_answers = [entry['english'] for entry in vocabularies]
    for item in vocabularies:
        rand = random.randint(0, 1)
        question = {
            'question': get_definition_gpt(item['english']) if rand == 1 else item['vietnamese'],
        }
        
        correct_answer = item['english']
        random_answers = random.sample(all_answers, 4)
        
        if correct_answer not in random_answers:
            random_answers.pop()
            random_answers.append(correct_answer)
        
        random.shuffle(random_answers)
        ans_true_index = random_answers.index(correct_answer)
        
        question['answers'] = random_answers
        question['ans_true'] = ans_true_index
        
        quiz.append(question)
    
    return quiz