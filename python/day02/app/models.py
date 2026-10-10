from dataclasses import dataclass, field


@dataclass(kw_only=True)
class DocumentChunk:
    index: int
    content: str
    char_count: int = field(init=False)

    def __post_init__(self):
        self.char_count = len(self.content)
