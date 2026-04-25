from config import merge

def test_nested_merge():
    d1 = {'app': {'host': 'localhost', 'port': 8080}}
    d2 = {'app': {'port': 9000}}
    res = merge(d1, d2)
    assert res['app']['host'] == 'localhost'
    assert res['app']['port'] == 9000
