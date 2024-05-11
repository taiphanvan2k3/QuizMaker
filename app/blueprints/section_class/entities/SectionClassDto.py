class SectionClassDto:
    def __init__(
        self,
        id: str,
        name: str,
        created_by: str,
        owner_avatar: str,
        created_at,
        vocab_count: int = 0,
    ):
        self.id = id
        self.name = name
        self.created_by = created_by
        self.created_at = created_at
        self.owner_avatar = owner_avatar
        self.vocab_count = vocab_count
