from calculator import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_zeros():
    assert add(0, 0) == 0

def test_add_negative_cancel():
    assert add(-1, 1) == 0

def test_add_large():
    assert add(1000000, 2000000) == 3000000

def test_add_both_negative():
    assert add(-5, -3) == -8