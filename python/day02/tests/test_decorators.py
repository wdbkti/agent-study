from collections.abc import Iterable

from app.chunker import iter_document_chunks
from app.pipeline import risk_keyword_rule, min_length_rule, ProcessChunkResult, process_chunks


def test_process_chunks_decorator(content, chunk_size, risk_keywords):
    """
    1. 不改变业务返回值
    2.  保留__name__
    """
    iter_result = process_chunks(
        chunks=iter_document_chunks(content, chunk_size),
        rules=[
            min_length_rule(5),
            risk_keyword_rule(risk_keywords)
        ]
    )
    assert isinstance(iter_result, Iterable)
    assert process_chunks.__name__ == 'process_chunks'
