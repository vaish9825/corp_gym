class User:
    def __init__(self, id): self.id = id
class DB:
    def get_users(self): return [User(i) for i in range(50)]
    def get_profile(self, user): return {'profile': 'data'}

def fetch_user_profiles(db):
    users = db.get_users()
    return [db.get_profile(u) for u in users] # N+1 query simulate
