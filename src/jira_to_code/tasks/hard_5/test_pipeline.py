from pipeline import process_logs
import inspect

def test_generator():
    class MockFile:
        def readlines(self): raise MemoryError()
        def __iter__(self): yield 'a\n'; yield 'b\n'
    res = process_logs(MockFile())
    assert inspect.isgenerator(res)
    assert list(res) == ['a', 'b']
