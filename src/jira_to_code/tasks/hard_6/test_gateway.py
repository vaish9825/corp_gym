from gateway import StripeGateway, PaymentGateway

def test_stripe_gateway():
    assert issubclass(StripeGateway, PaymentGateway)
    s = StripeGateway()
    assert s.charge(100) == 'Charged 100 via Stripe'
