import pytest
from pydantic import ValidationError

from python.day01.app.schemas import DocumentCreate


def test_document_create():
    dc = DocumentCreate(title="文档标题1", content="文档内容1", category="分类1", tags=["tag1", "tag2"],
                        source="renrendoc")
    assert dc.model_dump() == {'title': "文档标题1", 'content': "文档内容1", 'category': "分类1",
                               "tags": ["tag1", "tag2"],
                               "source": "renrendoc"}


def test_title_too_short():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(title="文")
    assert "type=string_too_short" in str(exc_info.value)


def test_title_too_long():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(
            title="文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1文档标题1")
    assert "type=string_too_long" in str(exc_info.value)


def test_content_empty():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(title="文档标题1", content="")
    assert "type=string_too_short" in str(exc_info.value)


def test_tags_short_boundary():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(title="文档标题1", content="文档内容1", category="分类1", tags=[])
    assert "type=too_short" in str(exc_info.value)


def test_tags_long_boundary():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(title="文档标题1", content="文档内容1", category="分类1",
                       tags=["tag1", "tag2", "tag1", "tag2", "tag1", "tag2", "tag1", "tag2", "tag1", "tag2", "tag1",
                             "tag2"])
    assert "type=too_long" in str(exc_info.value)


def test_source_missing():
    with pytest.raises(ValidationError) as exc_info:
        DocumentCreate(title="文档标题1", content="文档内容1", category="分类1", tags=["tag1", "tag2"])
    assert "type=missing" in str(exc_info.value)
