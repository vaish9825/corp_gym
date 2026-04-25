from lru_cache import LRUCache

def test_lru_cache_operations():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1       # returns 1
    cache.put(3, 3)                # evicts key 2
    assert cache.get(2) == -1      # returns -1 (not found)
    cache.put(4, 4)                # evicts key 1
    assert cache.get(1) == -1      # returns -1 (not found)
    assert cache.get(3) == 3       # returns 3
    assert cache.get(4) == 4       # returns 4

def test_cache_update_existing():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(1, 10)  # Update existing key
    assert cache.get(1) == 10
    assert cache.get(2) == -1  # never inserted

def test_cache_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)  # evicts key 1
    assert cache.get(1) == -1
    assert cache.get(2) == 2

def test_cache_get_refreshes_order():
    """get() should mark item as most recently used."""
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    cache.get(1)      # 1 is now most recently used
    cache.put(3, 3)   # Should evict 2, not 1
    assert cache.get(2) == -1
    assert cache.get(1) == 1
    assert cache.get(3) == 3

def test_cache_miss():
    cache = LRUCache(2)
    assert cache.get(999) == -1