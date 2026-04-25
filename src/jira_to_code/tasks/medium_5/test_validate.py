from validate import validate_email

def test_validate_email():
    assert validate_email('user@gmail.com') == True
    assert validate_email('user+test@gmail.com') == True
