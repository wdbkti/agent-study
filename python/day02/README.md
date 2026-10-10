# Day 2 - Decorator、Generator 与可测试的处理流水线

## 项目目标

继Day 01的目标，扩展学习工程化会用到的概念：

- Callable：函数也是对象，能当参数传递，也能当返回值
- Decorator：装饰器
- Generator / yield：理解惰性计算、一次产出一个结果
- pytest fixture + parametrization：将case进一步工程化

## 学习内容

- 函数也是对象 / Callable
- Decorator（装饰品）
- Generator / yield
- pytest fixture + parametrization

## 项目结构

app/
> __init__.py、models.py、chunker.py、exceptions.py、decorators.py、pipeline.py

tests/
> conftest.py、test_chunker.py、test_decorators.py、test_pipeline.py
> test_fixture_study.py、test_parametrize.py

## 数据流

DocumentChunk
→ iter_document_chunks()
→ process_chunks()

## 校验职责

- min_length_rule：检测最小长度
- risk_keyword_rule：检测包含风险关键词的chunk内容

## 安装

- 本项目使用`uv`管理 Python 环境和依赖
- 版本建议使用Python 3.12+
- 进入day02项目目录：`cd python/day02`
- 安装并同步项目依赖：
    - `uv sync`
    - `uv`会根据`pyproject.toml`和`uv.lock`安装项目所需依赖。
- 如果本机尚未安装`uv`，需要先安装`uv`，再执行上述命令。

## 测试

- 运行全部测试：`uv run pytest -q`
- 查看详细测试结果：`uv run pytest -v`
- 只运行chunker测试：`uv run pytest tests/test_chunker.py -v`
- 只运行pipeline测试：`uv run pytest tests/test_pipeline.py -v`
- 只运行decorators测试：`uv run pytest tests/test_decorators.py -v`
- 测试主要覆盖：
    - 正常 chunk：整除与不整除两种
    - chunk_size = 1
    - chunk_size <= 0
    - 空正文的既定语义
    - chunk index 连续
    - char_count 正确
    - 两种 rule 的通过/失败
    - 多 rule 组合
    - decorator 不改变业务返回值
    - decorator 保留 __name__

## 已知限制

- min_length_rule中计算长度方式为：len(content)

## Day 1 复盘
