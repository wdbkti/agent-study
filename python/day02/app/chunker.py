from collections.abc import Iterator

from .exceptions import InvalidContentError, InvalidChunkSizeError
from .models import DocumentChunk


def iter_document_chunks(content: str, chunk_size: int) -> Iterator[DocumentChunk]:
    if len(content) <= 0:
        raise InvalidContentError("内容不能为空")

    if chunk_size <= 0:
        raise InvalidChunkSizeError(chunk_size)

    for chunk_index, index in enumerate(range(0, len(content), chunk_size)):
        yield DocumentChunk(index=chunk_index, content=content[index: index + chunk_size])

