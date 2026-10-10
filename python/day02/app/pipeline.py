from dataclasses import dataclass, field
from collections.abc import Iterable

from app.models import DocumentChunk
from typing import Callable
from app.decorators import call_log, use_time, call_count
from app.chunker import iter_document_chunks

ChunkRule = Callable[[DocumentChunk], bool]


def min_length_rule(length: int) -> ChunkRule:
    """最小长度规则

    Args:
        length: 最小字符数，必须为正整数

    Returns:
        一个规则函数，接收 DocumentChunk，返回其内容长度是否 >= length。
        True 表示通过。
        False 表示不通过。
    """

    def rule(chunk: DocumentChunk) -> bool:
        if chunk.char_count >= length:
            return True
        rule.reason = f"长度小于：{length}"
        return False

    rule.rule_name = "min_length_rule"
    return rule


def risk_keyword_rule(keywords: list[str]) -> ChunkRule:
    """风险关键词规则

    Args:
        keywords: 风险关键词

    Returns:
        一个规则函数，接收 DocumentChunk，返回其内容是否包含风险关键词。
        True 表示通过(未命中关键词)。
        False 表示不通过(命中关键词)。
    """

    def rule(chunk: DocumentChunk) -> bool:
        for keyword in keywords:
            if keyword in chunk.content:
                rule.reason = f"存在风险关键词：{keyword}"
                return False
        return True

    rule.rule_name = "risk_keyword_rule"
    return rule


@dataclass(kw_only=True)
class ProcessChunkResult:
    index: int
    passed: bool = True
    rule_name: str = ""
    reason: str = ""


@use_time
@call_log
@call_count
def process_chunks(chunks: Iterable[DocumentChunk], rules: list[ChunkRule]) -> Iterable[ProcessChunkResult]:
    for chunk in chunks:
        result = ProcessChunkResult(index=chunk.index)
        for rule in rules:
            if not rule(chunk):
                result.passed = False
                result.rule_name = rule.rule_name
                result.reason = rule.reason
        yield result
