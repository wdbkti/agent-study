import pytest

from python.day01.app.exceptions import InvalidTitleError
from python.day01.app.schemas import DocumentCreate
from python.day01.app.service import create_document

# 合法的参数
payload = {'title': "文档标题1", 'content': "文档内容1", 'category': "分类1", 'tags': ["tag1", "tag2"],
           'source': "renrendoc"}


def test_create_document():
    dc = DocumentCreate(**payload)
    document = create_document(dc)
    result = {**payload, 'word_count': 1}
    assert document.__dict__ == result


def test_title_forbidden_test():
    with pytest.raises(InvalidTitleError) as exc_info:
        new_payload = {**payload, 'title': "文档标题1测试"}
        dc = DocumentCreate(**new_payload)
        create_document(dc)
    assert "不能包含违禁词" in exc_info.value.reason


def test_title_forbidden_adv():
    with pytest.raises(InvalidTitleError) as exc_info:
        new_payload = {**payload, 'title': "文档广告标题1"}
        dc = DocumentCreate(**new_payload)
        create_document(dc)
    assert "不能包含违禁词" in exc_info.value.reason


def test_title_forbidden_kj():
    with pytest.raises(InvalidTitleError) as exc_info:
        new_payload = {**payload, 'title': "课件文档标题1"}
        dc = DocumentCreate(**new_payload)
        create_document(dc)
    assert "不能包含违禁词" in exc_info.value.reason


def test_title_forbidden_kj_title():
    with pytest.raises(InvalidTitleError) as exc_info:
        new_payload = {**payload, 'title': "课件文档标题1"}
        dc = DocumentCreate(**new_payload)
        create_document(dc)
    assert exc_info.value.title == new_payload['title']


def test_title_forbidden_kj_forbidden_word():
    with pytest.raises(InvalidTitleError) as exc_info:
        new_payload = {**payload, 'title': "课件文档标题1"}
        dc = DocumentCreate(**new_payload)
        create_document(dc)
    assert exc_info.value.forbidden_word == '课件'


def test_title_forbidden_word_count():
    dc = DocumentCreate(**payload)
    document = create_document(dc)
    assert document.word_count == len(document.content)
