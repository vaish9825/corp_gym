def update_user_profile(db, redis, id, data):
    db.update(id, data)
