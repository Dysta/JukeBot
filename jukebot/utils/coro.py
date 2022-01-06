import asyncio


def run_threadsafe(coro, loop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        fut.result()
    except Exception as e:
        print(f"fut result exception {e=}")
