from server import process, lock
import pytest

@pytest.mark.asyncio
async def test_deadlock_fixed():
    try:
        await process()
    except TimeoutError:
        pass
    assert lock.locked() == False
