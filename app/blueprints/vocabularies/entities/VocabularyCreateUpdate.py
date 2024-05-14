class VocabularyCreateUpdate:
    def __init__(
        self, section_class_id: str, id, english_text, vietnamese_text, is_started
    ):
        self.section_class_id = section_class_id
        self.id = id
        self.english_text = english_text
        self.vietnamese_text = vietnamese_text
        self.is_started = is_started
