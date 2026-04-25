from service import fetch_rates
class MockClient:
    def get(self, url):
        raise TimeoutError()

def test_fetch_rates_fallback():
    assert fetch_rates(MockClient()) == {'USD': 1.0} # cached fallback
