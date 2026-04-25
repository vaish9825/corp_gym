from order import Order
import pytest

def test_invalid_transition():
    o = Order()
    o.state = 'CANCELLED'
    with pytest.raises(ValueError):
        o.transition('SHIPPED')
