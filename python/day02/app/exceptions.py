class InvalidContentError(Exception):
    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"文档chunk失败：{reason}")


class InvalidChunkSizeError(Exception):
    def __init__(self, chunk_size: int) -> None:
        self.chunk_size = chunk_size
        super().__init__(f"无效的块大小：{chunk_size}")
