class SectionClassCreateUpdate:
    def __init__(
        self,
        id=0,
        section_class_name: str = "",
        section_class_desc: str = "",
        vocabularies=None,
        is_public: bool = False,
    ):
        self.id = id
        self.section_class_name = section_class_name
        self.section_class_desc = section_class_desc
        self.vocabularies = vocabularies
        self.is_public = is_public
