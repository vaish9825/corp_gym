import re
def validate_email(email):
    match = re.match(r'^[a-zA-Z0-9.]+@[a-zA-Z0-9]+\.[a-zA-Z]+$', email)
    return bool(match)
