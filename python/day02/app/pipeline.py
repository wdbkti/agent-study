import time
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
        一个规则函数，接收 DocumentChunk，返回ProcessChunkResult。
    """

    def rule(chunk: DocumentChunk) -> ProcessChunkResult:
        result = ProcessChunkResult(index=chunk.index)
        if 0 < length <= chunk.char_count:
            return result

        result.passed = False
        result.rule_name = "min_length_rule"
        if length <= 0:
            result.reason = f"最小长度不能小于：{length}"
        else:
            result.reason = f"长度小于：{length}"
        return result

    return rule


def risk_keyword_rule(keywords: list[str]) -> ChunkRule:
    """风险关键词规则

    Args:
        keywords: 风险关键词

    Returns:
        一个规则函数，接收 DocumentChunk，返回ProcessChunkResult。
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
