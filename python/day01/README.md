# Day 1 - Document Intake Validator

## 项目目标
建立 Agent/AI 后端后面反复会用到的 5 个工程化概念：
- typing：让代码的输入输出“可描述、可检查、可让 IDE/框架理解”
- dataclass：快速定义“纯数据对象”
- Pydantic：把外部不可信输入变成经过校验的结构化 Python 对象
- Exception：让错误具有明确业务语义，而不是到处 return false / None
- pytest：用自动化测试证明代码真的符合要求

## 学习内容
- typing
- dataclass
- Pydantic
- Exception
- pytest

## 项目结构
app/
> __init__.py、models.py、schemas.py、exceptions.py、service.py

tests/
> test_schemas.py、test_service.py



## 数据流

DocumentCreate
→ create_document()
→ Document


## 校验职责
Pydantic：
- 输入数据的格式和结构是否合法

Service：
- 业务规则校验
- 构建数据结构

## 安装
- 本项目使用`uv`管理 Python 环境和依赖
- 版本建议使用Python 3.12+
- 进入day01项目目录：`cd python/day01`
- 安装并同步项目依赖：
  - `uv sync`
  - `uv`会根据`pyproject.toml`和`uv.lock`安装项目所需依赖。
- 如果本机尚未安装`uv`，需要先安装`uv`，再执行上述命令。

## 测试
- 运行全部测试：`uv run pytest -q`
- 查看详细测试结果：`uv run pytest -v`
- 只运行Schema测试：`uv run pytest tests/test_schemas.py -v`
- 只运行Service测试：`uv run pytest tests/test_service.py -v`
- 测试主要覆盖：
  - 正常文档创建
  - title长度边界
  - content为空
  - tags数量边界
  - source校验
  - 禁止标题业务规则
  - 自定义异常
  - word_count计算

## 已知限制
- Day 1 中 word_count 暂定义为 len(content)，即 Python 字符串字符数量；不进行中文分词，也不区分标点和空白。正式文库项目后续重新定义统计规则。

## Day 1 复盘
