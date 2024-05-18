class SectionClassDetailDto:
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        owner: dict,
        created_at: dict,
        vocabularies: list,
        is_public: bool = False,
        is_pending: bool = True
    ):
        self.id = id
        self.name = name
        self.description = description
        self.vocabularies = vocabularies
        self.owner = owner
        self.created_at = created_at
        self.is_public = is_public
        self.is_pending = is_pending
