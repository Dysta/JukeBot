import asyncio

from loguru import logger


def run_threadsafe(coro, loop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        fut.result()
    except Exception as e:
        logger.error(e)
