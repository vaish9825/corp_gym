from fastapi.testclient import TestClient
from routes import app

def test_billing_protected():
    client = TestClient(app)
    response = client.get('/api/billing')
    assert response.status_code == 401
