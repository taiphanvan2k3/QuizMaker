from ..utils.firestore_utils import initialize_firestore, firestore
from .entities.SectionClassCreateUpdate import SectionClassCreateUpdate
from .entities.SectionClassDto import SectionClassDto
from .entities.SectionClassDetailDto import SectionClassDetailDto
from flask import g
from datetime import datetime
import pytz
import random
from ..utils.openai import get_definition_gpt
from ..utils.helpers import get_time_diff

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
        # query = query.where("members.email", "==", current_user["email"])
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
            "members": [
                current_user["email"],
            ],
            "created_at": datetime.now(timezone),
            "vocab_count": len(section_class.vocabularies),
        }
    )

    # Ngay sau khi tạo lớp học phần, tạo sub-collection cho logs truy cập
    access_log_ref = (
        new_section_class_ref[1]
        .collection("members_access_logs")
        .document(current_user["email"])
    )
    access_log_ref.set({"logs": datetime.now(timezone)})

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
        ["name", "description", "created_at", "is_public", "members", "owner"]
    )
    if not section_class_doc.exists:
        return None

    # Cập nhật thời gian truy cập gần nhất
    last_accessed = datetime.now(timezone)
    current_user = g.user_info

    # Truy cập subcollection để cập nhật last_accessed
    log_ref = section_class_doc.reference.collection("members_access_logs").document(
        current_user["email"]
    )
    log_doc = log_ref.get()
    if log_doc.exists:
        # Cập nhật last_accessed nếu document đã tồn tại
        log_ref.update({"logs": last_accessed})
    else:
        # Tạo mới nếu chưa tồn tại
        log_ref.set({"logs": last_accessed})

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

    owner_info = section_class_doc.get("owner").get().to_dict()
    created_at = section_class_doc.get("created_at")

    is_pending = current_user["email"] not in section_class_doc.get("members")

    # Tìm độ chênh lệch về thời gian hiện tại với created_at
    return SectionClassDetailDto(
        section_class_id,
        section_class_doc.get("name"),
        section_class_doc.get("description"),
        owner={
            "display_name": owner_info["display_name"],
            "picture": owner_info["picture"],
        },
        created_at={
            "actual": created_at,
            "simple": get_time_diff(created_at, datetime.now(timezone)),
        },
        vocabularies=vocabularies,
        is_public=section_class_doc.get("is_public"),
        is_pending=is_pending,
    )


def create_quiz(vocabularies):
    quiz = []
    all_answers = [entry["english"] for entry in vocabularies]
    for item in vocabularies:
        rand = random.randint(0, 1)
        question = {
            "question": (
                get_definition_gpt(item["english"]) if rand == 1 else item["vietnamese"]
            ),
        }

        correct_answer = item["english"]
        random_answers = random.sample(all_answers, 4)

        if correct_answer not in random_answers:
            random_answers.pop()
            random_answers.append(correct_answer)

        random.shuffle(random_answers)
        ans_true_index = random_answers.index(correct_answer)

        question["answers"] = random_answers
        question["ans_true"] = ans_true_index

        quiz.append(question)

    return quiz


def get_recent_section_classes():
    current_user = g.user_info
    email = current_user["email"]

    # Truy vấn tất cả các section_class mà người dùng là thành viên
    query = section_class_ref.where("members", "array_contains", email).stream()

    sections = []
    for section in query:
        section_data = section.to_dict()
        owner = section_data["owner"].get()
        section_id = section.id
        section_data["display_name"] = owner.get("display_name")
        section_data["picture"] = owner.get("picture")
        section_data["id"] = section_id

        # Lấy thông tin last_accessed từ subcollection members_access_logs
        access_log_ref = (
            section_class_ref.document(section_id)
            .collection("members_access_logs")
            .document(email)
        )
        access_log = access_log_ref.get()
        if access_log.exists:
            last_accessed = access_log.to_dict()["logs"]
            section_data["user_last_accessed"] = last_accessed
            sections.append(section_data)

    # Sắp xếp các section dựa trên last_accessed của người dùng hiện tại
    sorted_sections = sorted(
        sections, key=lambda x: x["user_last_accessed"], reverse=True
    )

    # Lấy top 3
    recent_section_classes = sorted_sections[:3]

    return recent_section_classes


def get_all_members(id):
    current_section_class_ref = section_class_ref.document(id).get(
        ["members", "pending_members"]
    )
    if not current_section_class_ref.exists:
        return None
    data = current_section_class_ref.to_dict()
    member_emails = data.get("members", [])
    pending_member_emails = data.get("pending_members", [])

    members = get_members_info(member_emails)
    pending_members = []
    if len(pending_member_emails) > 0:
        pending_members = get_members_info(pending_member_emails)

    return {
        "members": members,
        "pending_members": pending_members,
    }


def get_members_info(emails):
    members = []
    for email in emails:
        user = db.collection("users").where("email", "==", email).stream()
        for user_data in user:
            user_data = user_data.to_dict()
            members.append(
                {
                    "display_name": user_data.get("display_name", email.split("@")[0]),
                    "picture": user_data.get("picture", ""),
                    "email": user_data["email"],
                }
            )
    return members


def share_to_user(id, email):
    current_section_class_ref = section_class_ref.document(id)
    current_section_class_ref.update({"pending_members": firestore.ArrayUnion([email])})

    # Lấy thông tin lớp học
    current_section_class_ref = current_section_class_ref.get()
    section_class_name = current_section_class_ref.to_dict().get("name")

    # Thêm vào collection user_notifications của user nhận
    user = db.collection("users").where("email", "==", email).get()
    sender_ref = db.collection("users").document(g.user_info["id"])
    sender_data = sender_ref.get()
    if user[0].exists and sender_data.exists:
        db.collection("user_notifications").document(user[0].id).collection(
            "notifications"
        ).add(
            {
                "type": "đã mời bạn vào lớp học phần",
                "section_class_id": id,
                "section_class_name": section_class_name,
                "from": sender_ref,
                "created_at": datetime.now(timezone),
                "is_seen": False,
            }
        )


# Update status của notification từ chưa xem thành đã xem
def update_notification_status(user_id, notification_id):
    notification_ref = (
        db.collection("user_notifications")
        .document(user_id)
        .collection("notifications")
        .document(notification_id)
    )
    notification_ref.update({"is_seen": True})


def response_invitation(section_class_id, is_accept):
    current_user = g.user_info
    section_class_ref = db.collection("section_class").document(section_class_id)

    # Xoá user này khỏi danh sách pending_members, đồng thời thêm vào members neu is_accept = True
    section_class_ref.update(
        {
            "pending_members": firestore.ArrayRemove([current_user["email"]]),
        }
    )

    if is_accept == "accept":
        section_class_ref.update(
            {
                "members": firestore.ArrayUnion([current_user["email"]]),
            }
        )
    else:
        # Update notification là reject để lát không thể vào lại lớp học phần này nữa
        notifications_ref = (
            db.collection("user_notifications")
            .document(current_user["id"])
            .collection("notifications")
        )
        query = notifications_ref.where(
            filter=("section_class_id", "==", section_class_id)
        ).where(filter=("is_seen", "==", True))

        results = query.stream()
        for result in results:
            result.reference.update({"status": "reject"})
