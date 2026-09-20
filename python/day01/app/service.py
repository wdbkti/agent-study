from .exceptions import InvalidTitleError
from .models import Document
from .schemas import DocumentCreate


def create_document(payload: DocumentCreate) -> Document:
    forbidden = ["测试", "课件", "广告"]
    for v in forbidden:
        if v in payload.title:
            raise InvalidTitleError(title=payload.title, reason="不能包含违禁词", forbidden_word=v)
    document = Document(**payload.model_dump())
    return document
