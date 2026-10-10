from pydantic import BaseModel, Field
from dataclasses import dataclass, field
import pytest


@dataclass(kw_only=True)
class Document:
    title: str
    content: str
    category: str
    tags: list[str]
    source: str
    word_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.word_count = len(self.content)


class DocumentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=20)
    content: str = Field(min_length=1)
    category: str
    tags: list[str] = Field(default_factory=list, max_length=10)
    source: str


class InvalidTitleError(ValueError):
    """包含违禁关键词"""

    def __init__(self, title: str, reason: str, forbidden_word: str) -> None:
        self.title = title
        self.reason = reason
        self.forbidden_word = forbidden_word
        super().__init__(f"{reason}，标题“{title}”存在违禁词：{forbidden_word}")


def create_document(payload: DocumentCreate) -> Document:
    forbidden = ["测试", "课件", "广告"]
    for v in forbidden:
        if v in payload.title:
            raise InvalidTitleError(title=payload.title, reason="不能包含违禁词", forbidden_word=v)
    document = Document(**payload.model_dump())
    return document


@pytest.fixture
def payload():
    return {'title': "文档标题1", 'content': "文档内容1", 'category': "分类1", 'tags': ["tag1", "tag2"],
            'source': "renrendoc"}


def test_create_document(payload):
    dc = DocumentCreate(**payload)
    document = create_document(dc)
    result = {**payload, 'word_count': 5}
    assert document.__dict__ == result


@pytest.mark.parametrize("title, exception, match", [
    ("文档标题1测试", InvalidTitleError, "存在违禁词：测试"),
    ("文档广告标题1", InvalidTitleError, "存在违禁词：广告"),
    ("课件文档标题1", InvalidTitleError, "存在违禁词：课件")
])
def test_title_forbidden_test(payload, title, exception, match):
    payload['title'] = title
    with pytest.raises(exception, match=match):
        list(create_document(DocumentCreate(**payload)))
