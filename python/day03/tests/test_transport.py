import math

import httpx
import pytest

from app.tool_client import WeatherToolClient
from httpx import ReadTimeout, ConnectError

from app.models import ToolResult
from app.transport import HttpxJsonTransport


class FakeJsonTransport:
    def __init__(self, payload: dict = None, exception: Exception = None) -> None:
        self.payload = payload
        self.exception = exception
        self.calls: list[tuple[str, float]] = []

    async def get_json(self, url: str, *, timeout: float = 5.0) -> dict:
        self.calls.append((url, timeout))
        if self.exception is not None:
            raise self.exception
        return self.payload


@pytest.fixture
def payload():
    return {"city": "beijing", "temperature": 18}


@pytest.mark.asyncio
@pytest.mark.parametrize("city", ["", "   ", "\t\n"])
async def test_city_empty(tool_result_data, city):
    fake = FakeJsonTransport(tool_result_data)
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather(city)

    assert isinstance(result, ToolResult)
    assert result.ok == False
    assert result.data is None
    assert result.error == "invalid_input"
    assert result.message == "无效的city"
    assert fake.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "city,expected",
    [
        ("Beijing", "beijing"),
        (" SHANGHAI ", "shanghai"),
        ("北京市", "%E5%8C%97%E4%BA%AC%E5%B8%82"),
        ("A & B", "a+%26+b"),
    ]
)
async def test_city_normalize(city, expected):
    fake = FakeJsonTransport({"city": city.strip().lower(), "temperature": 18})
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather(city)

    assert isinstance(result, ToolResult)
    assert result.ok == True
    assert result.data["city"] == city.strip().lower()
    assert expected in fake.calls[0][0]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "temperature,expected",
    [
        (20, 20),
        (0, 0),
        (-15.5, -15.5)
    ]
)
async def test_temperature(temperature, expected):
    fake = FakeJsonTransport({"city": "beijing", "temperature": temperature})
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather("beijing")

    assert result.ok is True
    assert result.data["temperature"] == expected
    assert isinstance(result.data["temperature"], (int, float))


@pytest.mark.asyncio
async def test_transport_call_once(tool_result_data):
    fake = FakeJsonTransport(tool_result_data)
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather(city="beijing")

    assert len(fake.calls) == 1
    assert fake.calls[0][1] == 5.0


@pytest.mark.asyncio
async def test_read_timeout():
    fake = FakeJsonTransport(exception=ReadTimeout("超时"))
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather(city="beijing")

    assert result.ok is False
    assert result.data is None
    assert result.error == "timeout"
    assert "请求超时" in result.message


@pytest.mark.asyncio
async def test_connect_error():
    fake = FakeJsonTransport(exception=ConnectError("网络错误"))
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather(city="beijing")

    assert result.ok is False
    assert result.data is None
    assert result.error == "network_error"
    assert "网络错误" in result.message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "http_code",
    [404, 503]
)
async def test_mock_transport_404(tool_result_data, http_code):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/weather"
        assert request.method == "GET"
        return httpx.Response(http_code, json=tool_result_data)

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.AsyncClient(transport=transport)
    httpx_json = HttpxJsonTransport(client=httpx_client)
    client = WeatherToolClient(transport=httpx_json, timeout=5.0)
    result = await client.get_weather(city="beijing")

    assert result.ok is False
    assert result.data is None
    assert result.error == "http_error"
    assert f"HTTP {http_code}" in result.message


@pytest.mark.asyncio
async def test_mock_transport_200_invalid_json():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/weather"
        assert request.method == "GET"
        return httpx.Response(200, headers={"content-type": "application/json"}, content=b'{"temperature": 18')

    transport = httpx.MockTransport(handler)
    httpx_client = httpx.AsyncClient(transport=transport)
    httpx_json = HttpxJsonTransport(client=httpx_client)
    client = WeatherToolClient(transport=httpx_json, timeout=5.0)
    result = await client.get_weather(city="beijing")

    assert result.ok is False
    assert result.data is None
    assert result.error == "invalid_json"
    assert "JSON 解析失败" in result.message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload,message",
    [
        (None, "响应不是 JSON 对象"),
        ([], "响应不是 JSON 对象"),
        ({"city": "beijing"}, "缺少 temperature 字段"),
        ({"city": "beijing", "temperature": "temperature"}, "temperature 必须是数字"),
        ({"city": "beijing", "temperature": True}, "temperature 必须是数字"),
        ({"city": "beijing", "temperature": float("nan")}, "temperature 必须是数字"),
        ({"city": "beijing", "temperature": float("inf")}, "temperature 必须是数字"),
        ({"city": "beijing", "temperature": float("-inf")}, "temperature 必须是数字"),
    ]
)
async def test_invalid_payload(payload, message):
    fake = FakeJsonTransport(payload)
    client = WeatherToolClient(transport=fake, timeout=5.0)
    result = await client.get_weather("beijing")

    assert result.ok is False
    assert result.data is None
    assert result.error == "invalid_payload"
    assert message in result.message
