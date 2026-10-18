import pytest
from app.guided_practice import add

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "a,b,expected",
    [
        (1, 2, 3),
        (4, 5, 9),
        (-5, 5, 0)
    ]
)
async def test_add(a: int, b: int, expected: int):
    assert await add(a, b) == expected
