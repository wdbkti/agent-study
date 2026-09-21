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
- 刚打开邮件时候，看到内容其实很懵逼的，基本上看不太懂，哈哈哈。
- 虽然 Python 的语法能看和代码能看懂大部分，但是工程化什么的完全不熟悉。更不用说什么typing、dataclass、Pydantic、pytest这些概念了。
- 跟着邮件里面的教学内容大致学了一遍后，有了基本的概念：
  - typing 主要是用于类型描述和静态检查，并不会自动进行运行时校验；
  - Pydantic 更适合作为外部数据进入系统时的校验层；
  - dataclass 更适合作为系统内部的领域数据对象；
  - 至于 Exception 和 pytest，有其他语言基础，倒是很好理解了；
- 对于考核的内容，对其中好几个要求感到迷茫/模糊：
  - 比如pytest测试“非法word_count或等价边界”，在我的理解里(学习dataclass后)，word_count是Document初始化后自动构建的值，怎么会存在所谓的非法边界？不太理解
  - 比如create_document中的非法标题，是在Pydantic中校验还是在业务层校验，一开始是放到Pydantic中的，后面又调整到了业务层。
- 测试也写得不是很合规(主要还是想偷懒，对 Python 中的数据类型的运用技巧还不太熟，熟悉技巧后其实才是最精明的偷懒)
  - 测试中出现过一个测试同时触发多个ValidationError的情况(其实我也明白数据没写全会触发多个错误，但是异常却刚好卡在我要验证那个场景，所以就没管)
  - 后来，改成先准备一份合法 payload，每个测试只修改一个字段，这样测试目标更明确(也是精明的偷懒，哈哈哈)
- 对于 uv 和 pytest 的使用也有了新的认识，特别是一个大目录下，多个子目录被划分为多个独立项目
  - 这让我意识到，一个项目上“代码能写出来” 和 “项目可以稳定运行、测试和复现”是两回事
- 以及 __init__.py 的作用，有它在，这个目录才算是一个包 (慢慢补充这方面的知识吧)
- 最后，总结一下我对 Day 1 的理解：
  - Pydantic 负责守住输入边界
  - Service 负责业务规则
  - dataclass 表示内部对象
  - 自定义异常 表达明确的失败原因
  - pytest 用来保证这些行为以后修改代码时不会被破坏
- 最后的最后，第一次写复盘，比较乱，哈哈哈，以后多复