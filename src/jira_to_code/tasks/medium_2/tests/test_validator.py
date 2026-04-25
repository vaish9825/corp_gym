from validator import validate_email, validate_password

def test_valid_email():
    assert validate_email("user@example.com") == True

def test_invalid_email_no_at():
    assert validate_email("userexample.com") == False

def test_invalid_email_no_dot():
    assert validate_email("user@examplecom") == False

def test_invalid_email_empty_local():
    assert validate_email("@example.com") == False

def test_invalid_email_double_at():
    assert validate_email("user@@example.com") == False

def test_valid_password():
    assert validate_password("Secret1234") == True

def test_short_password():
    assert validate_password("Sh1") == False

def test_no_uppercase_password():
    assert validate_password("secret1234") == False

def test_no_digit_password():
    assert validate_password("SecretPass") == False

def test_no_lowercase_password():
    assert validate_password("SECRET1234") == False
