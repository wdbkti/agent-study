import logging
import time
from collections.abc import Iterable
from functools import wraps

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def call_count(fn):
    """统计调用次数"""
    counter = {"count": 0}

    @wraps(fn)
    def wrapper(*args, **kwargs):
        wrapper.counter["count"] += 1
        return fn(*args, **kwargs)

    wrapper.counter = counter
    return wrapper


def use_time(fn):
    """记录执行耗时"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        logger.info("开始执行")
        r = fn(*args, **kwargs)
        if isinstance(r, Iterable):
            def counter_wrapper():
                try:
                    yield from r
                finally:
                    logger.info("结束执行")
                    logger.info("执行耗时%.4fs", time.perf_counter() - start)

            return counter_wrapper()
        logger.info("结束执行")
        logger.info("执行耗时%.4fs", time.perf_counter() - start)
        return r

    return wrapper


def call_log(fn):
    """输出统一调用日志"""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        logger.info("调用开始")
        r = fn(*args, **kwargs)
        logger.info("调用结束")
        return r

    return wrapper
