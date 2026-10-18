from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ToolResult:
    tool_name: str = "weather"
    ok: bool
    data: dict[str, object] | None = None
    error: str | None = None
    message: str | None = None

    @classmethod
    def success(cls, data: dict[str, object]) -> "ToolResult":
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, error: str, message: str) -> "ToolResult":
        return cls(ok=False, error=error, message=message)
