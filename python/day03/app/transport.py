from typing import Protocol

import httpx


class JsonTransport(Protocol):
    async def get_json(self, url: str, *, timeout: float = 5.0) -> object:
        ...


class HttpxJsonTransport:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def get_json(self, url: str, *, timeout: float = 5.0) -> object:
        response = await self.client.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
