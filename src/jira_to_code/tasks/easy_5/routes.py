from fastapi import FastAPI
app = FastAPI()
@app.get('/users/{user_id}')
def get_user(id: int):
    return {'user_id': id}
