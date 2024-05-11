class SectionClassDto:
    def __init__(
        self,
        id: str,
        name: str,
        created_by: str,
        owner_avatar: str,
        vocab_count: int = 0,
    ):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.owner_avatar = owner_avatar
        self.vocab_count = vocab_count
