from python.day01.app.exceptions import InvalidTitleError
from python.day01.app.models import Document
from python.day01.app.schemas import DocumentCreate


def create_document(payload: DocumentCreate) -> Document:
    document = Document(**payload.model_dump())
    forbidden = ["测试", "课件", "广告"]
    for v in forbidden:
        if v in payload.title:
            raise InvalidTitleError(title=v, reason="不能包含违禁词")
    return document
