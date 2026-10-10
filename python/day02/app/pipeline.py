from dataclasses import dataclass, field
from collections.abc import Iterable

from app.models import DocumentChunk
from typing import Callable
from app.decorators import call_log, use_time, call_count
from app.chunker import iter_document_chunks


@dataclass(kw_only=True)
class ProcessChunkResult:
    index: int
    passed: bool = True
    rule_name: str = ""
    reason: str = ""


ChunkRule = Callable[[DocumentChunk], ProcessChunkResult]


def min_length_rule(length: int) -> ChunkRule:
    """最小长度规则

    Args:
        length: 最小字符数，必须为正整数

    Returns:
        一个规则函数，接收 DocumentChunk，返回其内容长度是否 >= length。
        True 表示通过。
        False 表示不通过。
    """

    def rule(chunk: DocumentChunk) -> ProcessChunkResult:
        result = ProcessChunkResult(index=chunk.index)
        if chunk.char_count >= length:
            return result
        result.rule_name = "min_length_rule"
        result.reason = f"长度小于：{length}"
        result.passed = False
        return result

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

    def rule(chunk: DocumentChunk) -> ProcessChunkResult:
        result = ProcessChunkResult(index=chunk.index)
        for keyword in keywords:
            if keyword in chunk.content:
                result.rule_name = "risk_keyword_rule"
                result.reason = f"存在风险关键词：{keyword}"
                result.passed = False
                return result
        return result

    return rule


@use_time
@call_log
@call_count
def process_chunks(chunks: Iterable[DocumentChunk], rules: list[ChunkRule]) -> Iterable[ProcessChunkResult]:
    for chunk in chunks:
        result = ProcessChunkResult(index=chunk.index)
        for rule in rules:
            result = rule(chunk)
            if not result.passed:
                break
        yield result
