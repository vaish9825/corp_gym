from fastapi.testclient import TestClient
from routes import app

def test_get_user():
    client = TestClient(app)
    response = client.get('/users/42')
    assert response.status_code == 200
    assert response.json() == {'user_id': 42}
