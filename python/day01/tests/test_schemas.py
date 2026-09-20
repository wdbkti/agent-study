import pytest
from pydantic import ValidationError

from app.schemas import DocumentCreate

payload = {'title': "文档标题1", 'content': "文档内容1", 'category': "分类1", 'tags': ["tag1", "tag2"],
           'source': "renrendoc"}


def test_document_create():
    dc = DocumentCreate(**payload)
    assert dc.model_dump() == payload


def test_title_too_short():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload, 'title': '文'}
        DocumentCreate(**new_payload)
    assert "type=string_too_short" in str(exc_info.value)


def test_title_too_long():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload,
                       'title': '文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1'}
        DocumentCreate(**new_payload)
    assert "type=string_too_long" in str(exc_info.value)


def test_content_empty():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload, 'content': ""}
        DocumentCreate(**new_payload)
    assert "type=string_too_short" in str(exc_info.value)


def test_tags_1():
    new_payload = {**payload, 'tags': ['tag1']}
    dc = DocumentCreate(**new_payload)
    assert dc.model_dump() == new_payload


def test_tags_short_boundary():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload, 'tags': []}
        DocumentCreate(**new_payload)
    assert "type=too_short" in str(exc_info.value)


def test_tags_long_boundary():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload,
                       'tags': ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10",
                                "tag11"]}
        DocumentCreate(**new_payload)
    assert "type=too_long" in str(exc_info.value)


def test_source_missing():
    with pytest.raises(ValidationError) as exc_info:
        new_payload = {**payload}
        del new_payload['source']
        DocumentCreate(**new_payload)
    assert "type=missing" in str(exc_info.value)
