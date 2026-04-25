from formatter import format_user_data

def test_format_full_data():
    data = {"first_name": "john", "last_name": "doe", "age": 30}
    assert format_user_data(data) == "DOE, John (Age: 30)"

def test_format_missing_age():
    data = {"first_name": "alice", "last_name": "smith"}
    assert format_user_data(data) == "SMITH, Alice (Age: Unknown)"

def test_format_already_capitalized():
    data = {"first_name": "BOB", "last_name": "JONES", "age": 25}
    assert format_user_data(data) == "JONES, Bob (Age: 25)"

def test_format_mixed_case():
    data = {"first_name": "jAnE", "last_name": "mCdOnAlD", "age": 0}
    assert format_user_data(data) == "MCDONALD, Jane (Age: 0)"