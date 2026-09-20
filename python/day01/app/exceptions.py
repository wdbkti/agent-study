class InvalidTitleError(ValueError):
    """包含违禁关键词"""
    def __init__(self, title: str, reason: str, forbidden_word: str):
        self.title = title
        self.reason = reason
        self.forbidden_word = forbidden_word
        super().__init__(reason)