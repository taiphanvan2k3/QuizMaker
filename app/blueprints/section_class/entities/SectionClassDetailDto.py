class SectionClassDetailDto:
    def __init__(
        self, id: str, name: str, owner: dict, created_at: dict, vocabularies: list
    ):
        self.id = id
        self.name = name
        self.vocabularies = vocabularies
        self.owner = owner
        self.created_at = created_at
