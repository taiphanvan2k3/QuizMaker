from ..utils.firestore_utils import initialize_firestore
from .entities.VocabularyCreateUpdate import VocabularyCreateUpdate

db = initialize_firestore()


def update_vocabulary(vocabulary: VocabularyCreateUpdate):
    vocabularies_ref = (
        db.collection("section_class")
        .document(vocabulary.section_class_id)
        .collection("vocabularies")
    )

    # Update vocabulary
    vocabularies_ref.document(vocabulary.id).update(
        {
            "english": vocabulary.english_text,
            "vietnamese": vocabulary.vietnamese_text,
            "is_stared": True if vocabulary.is_stared == "true" else False,
        }
    )


def get_list_vocabularies(section_class_id: str):
    vocabularies_ref = (
        db.collection("section_class")
        .document(section_class_id)
        .collection("vocabularies")
        .order_by("order", direction="ASCENDING")
        .stream()
    )

    vocabularies = []
    for vocabulary in vocabularies_ref:
        vocabularies.append(
            {
                "id": vocabulary.id,
                "english": vocabulary.to_dict()["english"],
                "vietnamese": vocabulary.to_dict()["vietnamese"],
            }
        )
    return vocabularies
