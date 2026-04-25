from fastapi import FastAPI
from auth import require_auth
app = FastAPI()
@app.get('/api/billing')
def get_billing():
    return {'billing': 'data'}
