import pytest
from app.models import DocumentChunk
from app.pipeline import process_chunks

_last_func = {"name": ""}


def pytest_runtest_setup(item):
    """每个测试 setup 时调用"""
    print(item)
    name = f"{item.module.__name__}::{item.originalname}"
    print(name)
    if "process_chunks" in name and _last_func["name"] != name:
        process_chunks.counter["count"] = 0
        _last_func["name"] = name


@pytest.fixture(scope="module")
def content():
    return "2026华为机考试题及答案一、单项选择题（每题2分，共10题）1.下列哪种数据结构适合实现队列？A.栈B.链表C.哈希表答案：B2.以下哪种排序算法平均时间复杂度为O(nlogn)？A.冒泡排序B.快速排序C.插入排序答案：B3.若一个int型变量占4字节，其能表示的最大数是？A.2^31-1B.2^32-1C.2^16-1答案：A"


@pytest.fixture(scope="module")
def chunk_size():
    return 10


@pytest.fixture(scope="module")
def risk_keywords():
    return ["广告", "课件", "考试", "答案"]


@pytest.fixture
def document_chunk_payload():
    return {"index": 0, "content": "这是一个文档的块"}


@pytest.fixture
def document_chunk(document_chunk_payload):
    return DocumentChunk(**document_chunk_payload)
