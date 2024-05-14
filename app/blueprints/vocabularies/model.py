from ..utils.firestore_utils import initialize_firestore
from .entities.VocabularyCreateUpdate import VocabularyCreateUpdate

db = initialize_firestore()


def update_vocabulary(vocabulary: VocabularyCreateUpdate):
    vocabularies_ref = (
        db.collection("section_class")
        .document(vocabulary.section_class_id)
        .collection("vocabularies")
    )

    print(bool(vocabulary.is_started))

    # Update vocabulary
    vocabularies_ref.document(vocabulary.id).update(
        {
            "english": vocabulary.english_text,
            "vietnamese": vocabulary.vietnamese_text,
            "is_stared": True if vocabulary.is_started == "true" else False,
        }
    )

    print("Vocabulary updated")
