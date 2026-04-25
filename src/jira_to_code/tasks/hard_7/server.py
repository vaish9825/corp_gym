import asyncio
import threading
lock = threading.Lock()
async def process():
    lock.acquire()
    raise TimeoutError()
    lock.release()
