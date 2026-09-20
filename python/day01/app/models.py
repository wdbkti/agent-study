from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Document:
    title: str
    content: str
    category: str
    tags: list[str]
    source: str
    word_count: int = field(init=False)

    def __post_init__(self):
        self.word_count = len(self.content.split())
