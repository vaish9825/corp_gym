from pagination import get_page_bounds

def test_get_page_bounds():
    assert get_page_bounds(1, 10) == (0, 10)
    assert get_page_bounds(2, 10) == (10, 20)
