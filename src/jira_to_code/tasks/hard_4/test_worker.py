from worker import Worker
import queue

def test_uses_queue():
    w = Worker()
    assert hasattr(w, 'jobs') and isinstance(w.jobs, queue.Queue)
