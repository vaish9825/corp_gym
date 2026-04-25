from orm import fetch_user_profiles, DB

def test_fetch_with_join():
    db = DB()
    db.get_profile = lambda _: '#FAIL' # simulate strict join mode
    profiles = fetch_user_profiles(db)
    assert '#FAIL' not in profiles
