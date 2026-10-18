import pytest

from app.models import ToolResult
from app.tool_client import parse_weather, WeatherToolClient

from tests.test_transport import FakeJsonTransport


def test_tool_result_success(tool_result_data):
    data = tool_result_data
    tr = ToolResult.success(data=data)
    assert tr.ok == True
    assert tr.data == data
    assert tr.error is None
    assert tr.message is None


def test_tool_result_failure():
    tr = ToolResult.failure(error="timeout", message="请求超时")
    assert tr.ok == False
    assert tr.data is None
    assert tr.error == "timeout"
    assert tr.message == "请求超时"


@pytest.mark.parametrize(
    "city, payload",
    [
        ("beijing", {"temperature": 18}),
        ("chengdu", {"temperature": 26}),
        ("heilongjiang", {"temperature": -5}),
        ("xinjiang", {"temperature": 0}),
    ]
)
def test_parse_weather_ok(city, payload):
    tr = parse_weather(payload, city)
    assert tr.ok == True
    assert tr.data == {**payload, "city": city}
    assert tr.error is None
    assert tr.message is None


@pytest.mark.parametrize(
    "payload, error,message",
    [
        ("", "invalid_payload", "响应不是 JSON 对象"),
        ({}, "invalid_payload", "缺少 temperature 字段"),
        ({"temperature": ""}, "invalid_payload", "temperature 必须是数字"),
        ({"temperature": True}, "invalid_payload", "temperature 必须是数字"),
        ({"temperature": False}, "invalid_payload", "temperature 必须是数字"),
        ({"temperature": {}}, "invalid_payload", "temperature 必须是数字"),
        ({"temperature": []}, "invalid_payload", "temperature 必须是数字"),
    ]
)
def test_parse_weather_exception(payload, error, message):
    tr = parse_weather(payload, "xinjiang")
    assert tr.ok == False
    assert tr.data is None
    assert tr.error == error
    assert tr.message == message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "timeout,message",
    [
        ("5秒", "必须是数字"),
        (0, "timeout 必须是有限正数"),
        (-5, "timeout 必须是有限正数"),
        (float("-inf"), "timeout 必须是有限正数"),
        (float("inf"), "timeout 必须是有限正数"),
        (float("nan"), "timeout 必须是有限正数"),
    ]
)
async def test_weather_timeout(timeout, message):
    fake = FakeJsonTransport()
    with pytest.raises(ValueError) as exc_info:
        client = WeatherToolClient(fake, timeout=timeout)

    assert message in str(exc_info.value)


@pytest.mark.asyncio
async def test_extra_fields_ignored():
    fake = FakeJsonTransport(
        payload={
            "city": "xinjiang",
            "temperature": 22.5,
            "humidity": 80,
            "extra": {"nested": True},
        }
    )
    client = WeatherToolClient(transport=fake)

    result = await client.get_weather("Beijing")

    assert result.ok is True
    assert result.data == {"city": "Beijing", "temperature": 22.5}
