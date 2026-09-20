import pytest

from python.day01.app.exceptions import InvalidTitleError
from python.day01.app.schemas import DocumentCreate
from python.day01.app.service import create_document


def test_create_document():
    dc = DocumentCreate(title="文档标题1", content="文档内容1", category="分类1", tags=["tag1", "tag2"],
                        source="renrendoc")
    document = create_document(dc)
    assert document.__dict__ == {'title': '文档标题1', 'content': '文档内容1', 'category': '分类1',
                                 'tags': ['tag1', 'tag2'], 'source': 'renrendoc', 'word_count': 1}


def test_title_forbidden():
    with pytest.raises(InvalidTitleError) as exc_info:
        dc = DocumentCreate(title="文档标题1测试", content="文档内容1", category="分类1", tags=["tag1", "tag2"],
                            source="renrendoc")
        create_document(dc)
    assert "不能包含违禁词" in exc_info.value.reason
