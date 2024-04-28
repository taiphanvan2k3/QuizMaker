from ..utils.firestore_utils import initialize_firestore

db = initialize_firestore()
section_class_ref = db.collection("section_class")


class SectionClass:
    def __init__(
        self, id: str, name: str, created_by: str, created_at, vocab_count: int = 0
    ):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.created_at = created_at
        self.vocab_count = vocab_count


def get_all_section_classes(section_type="all") -> list[SectionClass]:
    current_user = "taiphanvan2403"

    query = section_class_ref
    if section_type != "all": # các lớp học phần tự tạo
        query = query.where("created_by.username", "==", current_user)

    # Chỉ hiển thị các lớp học phần mà user này có tham gia
    query = query.where("members", "array_contains", current_user)

    # Dùng stream() thay vì get() để giúp nhận dữ liệu một cách tuần tự thay vì 
    # nhận toàn bộ dữ liệu một lúc khi dùng get()
    sections = query.stream()

    section_classes = []
    for section in sections:
        section_data = section.to_dict()
        section_classes.append(
            SectionClass(
                section.id,
                section_data["name"],
                section_data["created_by"]["display_name"],
                section_data["created_at"],
            )
        )

        # Truy cập sub-collection vocabularies
        vocabularies = section.reference.collection("vocabularies").get()
        section_classes[-1].vocab_count = len(list(vocabularies))

    if section_type != "all":
        section_classes = [section_classes[0]]
    return section_classes
