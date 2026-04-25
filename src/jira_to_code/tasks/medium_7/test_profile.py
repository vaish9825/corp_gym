from profile import update_user_profile
class MockRedis:
    def __init__(self): self.deleted = False
    def delete(self, key): self.deleted = True

def test_cache_invalidation():
    r = MockRedis()
    update_user_profile(None, r, 1, {})
    assert r.deleted == True
