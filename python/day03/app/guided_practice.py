import asyncio

async def add(a: int, b: int) -> int:
    await asyncio.sleep(0.1)
    return a + b

