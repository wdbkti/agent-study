import pytest

from app.exceptions import InvalidContentError, InvalidChunkSizeError
from app.models import DocumentChunk
from app.chunker import iter_document_chunks


def test_document_chunk(document_chunk_payload, document_chunk):
    new_payload = {**document_chunk_payload, "char_count": 8}
    assert document_chunk.__dict__ == new_payload


def test_iter_document_chunks(content, chunk_size):
    """正常的chunk 且 正文长度整数"""
    iter_chunks = iter_document_chunks(content, chunk_size)
    for index, chunk in enumerate(iter_chunks):
        assert isinstance(chunk, DocumentChunk)
        # chunk index连续
        assert chunk.index == index
        ## char_count正确
        assert chunk.char_count == len(chunk.content)


def test_iter_document_chunks2(chunk_size):
    """正文长度不整数"""
    iter_chunks = iter_document_chunks("这是一个文档的块长度不整除", chunk_size)
    for index, chunk in enumerate(iter_chunks):
        assert isinstance(chunk, DocumentChunk)
        # chunk index连续
        assert chunk.index == index
        ## char_count正确
        assert chunk.char_count == len(chunk.content)


def test_iter_document_chunks_empty_content(chunk_size):
    """正文为空"""
    iter_chunks = iter_document_chunks("", chunk_size)
    with pytest.raises(InvalidContentError) as exc_info:
        next(iter_chunks)
    assert "内容不能为空" in str(exc_info.value)


def test_iter_document_chunks_size1(content):
    """chunk_size 等于 1"""
    chunk_size = 1
    iter_chunks = iter_document_chunks(content, chunk_size)
    for index, chunk in enumerate(iter_chunks):
        assert isinstance(chunk, DocumentChunk)
        # chunk index连续
        assert chunk.index == index
        ## char_count正确
        assert chunk.char_count == chunk_size


def test_iter_document_chunks_error_size(content):
    """chunk_size 等于 0"""
    iter_chunks = iter_document_chunks(content, 0)
    with pytest.raises(InvalidChunkSizeError) as exc_info:
        next(iter_chunks)
    assert "无效的块大小：0" in str(exc_info.value)


def test_iter_document_chunks_error_size2(content):
    """chunk_size 小于 0"""
    iter_chunks = iter_document_chunks(content, -1)
    with pytest.raises(InvalidChunkSizeError) as exc_info:
        next(iter_chunks)
    assert "无效的块大小：-1" in str(exc_info.value)
