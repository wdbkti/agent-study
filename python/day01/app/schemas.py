from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=20)
    content: str = Field(min_length=1)
    category: str
    tags: list[str] = Field(default_factory=list, min_length=1, max_length=10)
    source: str
