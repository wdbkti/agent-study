# Day 3 — async/await、asyncio 与可测试的 HTTP Tool Client

## 项目目标

继Day 02的目标，扩展学习工程化会用到的概念：

- async/await：区分协程函数、协程对象、实际执行，以及事件循环
- asyncio：会使用 run、sleep、gather，区分顺序等待与并发等待
- HTTPX：会使用 AsyncClient、async with、状态码检查、JSON 和 timeout
- 可替换的依赖：理解 Protocol 和 FakeTransport，让业务测试脱离真实网络
- 错误边界：把超时、连接失败、HTTP 失败、JSON 失败和字段错误区分清楚
- 异步测试：在 pytest 中真正 await，并延续 Day 02 的 fixture/parametrize

## 学习内容

- async/await 协程
- asyncio
- HTTPX
- Protocol

## 项目结构

app/
> __init__.py、guided_practice.py、models.py、tool_client.py、transport.py

tests/
> conftest.py、test_tool_client.py、test_transport.py
> test_guided_practice.py

## 数据流

city
→ 输入规范化
→ WeatherToolClient
→ JsonTransport
→ HttpxJsonTransport
→ AsyncClient

## 校验职责

- city：去除首尾空白/空格后，不能为空

## 安装

- 本项目使用`uv`管理 Python 环境和依赖
- 版本建议使用Python 3.12+
- 进入day03项目目录：`cd python/day03`
- 安装并同步项目依赖：
    - `uv sync`
    - `uv`会根据`pyproject.toml`和`uv.lock`安装项目所需依赖。
- 如果本机尚未安装`uv`，需要先安装`uv`，再执行上述命令。

## 测试

- 运行全部测试：`uv run pytest -q`
- 查看详细测试结果：`uv run pytest -v`
- 只运行 guided_practice 测试：`uv run pytest tests/test_guided_practice.py -v`
- 只运行 tool_client 测试：`uv run pytest tests/test_tool_client.py -v`
- 只运行 transport 测试：`uv run pytest tests/test_transport.py -v`
- 测试主要覆盖：
    - 正常整数与小数温度，断言 ToolResult 全部关键字段。
    - 0 和负温度成功，False/True 不能被当成数值温度。
    - city="" 和纯空白失败，断言 Fake.calls 为空。
    - city 去首尾空白、中文、空格或 & 的编码；解析 URL 后断言参数原值，不只查 URL 包含一个单词。
    - 验证配置的 timeout 确实传入，且每次调用只发一次请求。
    - Fake 抛 ReadTimeout，结果为 timeout；Fake 抛 ConnectError，结果为 network_error。
    - 通过 MockTransport 返回 404/503，验证适配器会抛 HTTPStatusError，并至少验证一条接到业务层成为 http_error 的完整链路。
    - 通过 MockTransport 返回 200 + 非法 JSON，得到 invalid_json；不能用 Fake 直接返回 dict 来声称测过 JSON 解码。
    - 合法 JSON 但顶部为 list/null、缺少 temperature、值是字符串/bool/NaN/无穷大时，得到 invalid_payload；可以用 Fake
      构造这些业务层输入。
    - timeout 配置为 0/负数/非有限数时构造失败；用 pytest.raises(ValueError)。
    - 每个失败结果都检查 ok=False、data=None、error 正确、message 非空；至少一处有意义的 fixture 和参数化。
    - 适配器请求路径与方法正确；客户端由调用方 async with 管理。选任意一个参数化 case 独立运行仍通过。

## 已知限制

- 暂无

## Day 3 复盘

- 本次的主要学习点（之前有基础，基本看一眼就能知道具体是学个什么东西）：
    - async/await：区分协程函数、协程对象、实际执行，以及事件循环
    - asyncio：会使用 run、sleep、gather，区分顺序等待与并发等待
    - HTTPX：会使用 AsyncClient、async with、状态码检查、JSON 和 timeout
    - 可替换的依赖：理解 Protocol 和 FakeTransport，让业务测试脱离真实网络
    - 错误边界：把超时、连接失败、HTTP 失败、JSON 失败和字段错误区分清楚
    - 异步测试：在 pytest 中真正 await，并延续 Day 02 的 fixture/parametrize
- 由于有之前的底子，本次考核内容还是相对较为容易的。
- 本次实战是基于真实场景来，一开始还是会比较模糊，主要是各个知识点感觉都学会了，但当要将其揉合在一直子反倒有点不知道怎么下手了。
    - 先是按数据流，将各块功能实现，最后，再进行组装的
    - 测试的时候，才发现自己对于 FakeTransport 和 HttpxJsonTransport 其实还是模糊的，通过这里又加深了印象
        - 口试题也有提到，印象又更深了
        - FakeTransport 是属于业务层
        - HttpxJsonTransport 是属于 httpx 的 transport，属于适配器层
