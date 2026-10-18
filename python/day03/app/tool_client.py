import json
import math

import httpx

from app.models import ToolResult
from app.transport import JsonTransport


def parse_weather(payload: dict, city: str) -> ToolResult:
    if not isinstance(payload, dict):
        return ToolResult.failure("invalid_payload", "响应不是 JSON 对象")

    if "temperature" not in payload:
        return ToolResult.failure("invalid_payload", "缺少 temperature 字段")

    temperature = payload.get("temperature")
    if isinstance(temperature, bool) or not isinstance(temperature, (int, float)) or not math.isfinite(temperature):
        return ToolResult.failure("invalid_payload", "temperature 必须是数字")

    return ToolResult.success(
        {
            "city": city,
            "temperature": float(temperature),
        }
    )


class WeatherToolClient:
    base_url = "https://training.invalid/weather"

    def __init__(self, transport: JsonTransport, *, timeout: float = 5.0) -> None:
        if not isinstance(timeout, (float, int)):
            raise ValueError("timeout 必须是数字")
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError("timeout 必须是有限正数")

        self.transport = transport
        self.timeout = timeout

    async def get_weather(self, city: str) -> ToolResult:
        city = city.strip()
        if not city:
            return ToolResult.failure("invalid_input", "无效的city")


        url = str(httpx.URL(self.base_url, params={"city": city}))
        try:
            payload = await self.transport.get_json(url, timeout=self.timeout)
        except httpx.TimeoutException as e:
            return ToolResult.failure("timeout", f"请求超时：{e}")
        except httpx.HTTPStatusError as e:
            return ToolResult.failure("http_error", f"HTTP {e.response.status_code}: {e}")
        except httpx.RequestError as e:
            return ToolResult.failure("network_error", f"网络错误： {type(e).__name__}: {e}")
        except json.JSONDecodeError as e:
            return ToolResult.failure("invalid_json", f"JSON 解析失败：{e}")

        return parse_weather(payload, city)
