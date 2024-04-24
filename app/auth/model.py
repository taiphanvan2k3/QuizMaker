from ..utils.firestore_utils import initialize_firestore

db = initialize_firestore()
section_class_ref = db.collection("section_class")


def get_all_section_classes():
    sections = section_class_ref.get()
    section_classes = []
    for section in sections:
        section_data = section.to_dict()
        section_classes.append(
            {"name": section_data["name"], "created_by": section_data["created_by"]}
        )
    return section_classes
