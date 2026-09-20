from pydantic import BaseModel, Field, field_validator

from python.day01.app.exceptions import InvalidTitleError


class DocumentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=20)
    content: str = Field(min_length=1)
    category: str
    tags: list[str] = Field(default_factory=list, min_length=1, max_length=10)
    source: str

    """
    @field_validator('title')
    @classmethod
    def title_must_not_be_forbidden(cls, v: str) -> str:
        forbidden = ["测试", "课件", "广告"]
        for iv in forbidden:
            if iv in v:
                raise InvalidTitleError(title=v, reason="不能包含违禁词")
        return v
    """