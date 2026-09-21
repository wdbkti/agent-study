import pytest

from app.exceptions import InvalidTitleError
from app.schemas import DocumentCreate
from app.service import create_document

# 合法的参数
payload = {'title': "文档标题1", 'content': "文档内容1", 'category': "分类1", 'tags': ["tag1", "tag2"],
           'source': "renrendoc"}


def test_create_document():
    dc = DocumentCreate(**payload)
    document = create_document(dc)
    result = {**payload, 'word_count': 5}
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


def test_word_count():
    dc = DocumentCreate(**payload)
    document = create_document(dc)
    assert document.word_count == len(document.content)


def test_normal_data_1():
    new_payload = {**payload, 'title': "中央空调机组操作SOP",
                   'content': "确保参数设定符合实际使用需求，为后续启动奠定基础", 'category': "操作手册",
                   'tags': ["手册"], 'source': '人人文库'}
    dc = DocumentCreate(**new_payload)
    document = create_document(dc)
    assert document.word_count == len(document.content)


def test_normal_data_2():
    new_payload = {**payload, 'title': "政务信息资源目录体系",
                   'content': "政务信息资源目录体系是政务信息资源开发和利用的基础设施，主要介绍了 包括政务信息资源目录体系的基本概念、主要作用、关键标准、支撑技术及应用模 式。关键字：信息资源目录3关键标准31主要内容政务信息资",
                   'category': "其他文档",
                   'tags': ["资源目录"], 'source': 'max'}
    dc = DocumentCreate(**new_payload)
    document = create_document(dc)
    assert document.word_count == len(document.content)
