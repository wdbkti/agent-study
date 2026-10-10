from collections.abc import Iterable

import pytest
from app.pipeline import risk_keyword_rule, min_length_rule, ProcessChunkResult, process_chunks
from app.models import DocumentChunk
from app.chunker import iter_document_chunks


@pytest.mark.parametrize(
    "risk_keyword,expected",
    [
        ("答案", False),
        ("考试", False),
        ("学习", True),
        ("测试", True)
    ]
)
def test_risk_keyword_rule(risk_keywords, document_chunk, risk_keyword, expected):
    """有风险词，未通过"""
    document_chunk.content += risk_keyword
    r = risk_keyword_rule(risk_keywords)(document_chunk)
    assert r.passed == expected


@pytest.mark.parametrize(
    "min_length,expected",
    [
        (5, True),
        (20, False),
    ]
)
def test_min_length_rule(document_chunk, min_length, expected):
    """最小长度"""
    r = min_length_rule(min_length)(document_chunk)
    assert r.passed == expected


@pytest.fixture
def process_chunk_result():
    return {"index": 0, "passed": True, "rule_name": "", "reason": ""}


def test_process_chunk_result_pass(process_chunk_result):
    result = ProcessChunkResult(**process_chunk_result)
    assert result.__dict__ == process_chunk_result


def test_process_chunk_result_not_pass(process_chunk_result):
    process_chunk_result["passed"] = False
    process_chunk_result["rule_name"] = "risk_keyword_rule"
    result = ProcessChunkResult(**process_chunk_result)
    assert result.__dict__ == process_chunk_result


def test_process_chunks(content, chunk_size, risk_keywords):
    iter_result = process_chunks(
        chunks=iter_document_chunks(content, chunk_size),
        rules=[
            min_length_rule(5),
            risk_keyword_rule(risk_keywords)
        ]
    )
    assert process_chunks.__name__ == "process_chunks"
    assert process_chunks.counter["count"] == 1
    for index, result in enumerate(iter_result):
        assert isinstance(result, ProcessChunkResult)


@pytest.mark.parametrize(
    "content,passed,rule_name,reason,call_count",
    [
        ("这个文档块有广告内容", False, "risk_keyword_rule", "存在风险关键词：广告", 1),
        ("这个文档块有课件pdf", False, "risk_keyword_rule", "存在风险关键词：课件", 2),
        ("这个文档块没有非法词", True, "", "", 3),
        ("这个文档块", False, "min_length_rule", "长度小于：10", 4)
    ]
)
def test_process_chunks_multi_rule(
        chunk_size, risk_keywords, content, passed, rule_name, reason, call_count
):
    """"多rule组合"""
    iter_result = process_chunks(
        chunks=iter_document_chunks(content, chunk_size),
        rules=[
            min_length_rule(chunk_size),
            risk_keyword_rule(risk_keywords)
        ]
    )
    assert process_chunks.__name__ == "process_chunks"
    assert process_chunks.counter["count"] == call_count

    result = next(iter_result)
    assert isinstance(result, ProcessChunkResult)
    assert result.passed == passed
    assert result.rule_name == rule_name
    assert reason in result.reason


def test_process_chunks_all_fail(chunk_size, risk_keywords):
    """首个失败即停止检测"""
    content = "这就是广告内容"
    iter_result = process_chunks(
        chunks=iter_document_chunks(content, chunk_size),
        rules=[
            min_length_rule(chunk_size),
            risk_keyword_rule(risk_keywords)
        ]
    )

    assert isinstance(iter_result, Iterable)

    chunk = next(iter_result)
    assert isinstance(chunk, ProcessChunkResult)
    assert chunk.index == 0
    assert chunk.passed is False
    assert chunk.rule_name == "min_length_rule"
    assert chunk.reason == "长度小于：10"
