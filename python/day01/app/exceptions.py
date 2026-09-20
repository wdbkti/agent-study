class InvalidTitleError(ValueError):
    """包含违禁关键词"""
    def __init__(self, title: str, reason: str):
        self.title = title
        self.reason = reason