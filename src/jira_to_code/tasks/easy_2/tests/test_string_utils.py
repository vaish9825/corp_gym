from string_utils import count_vowels

def test_lowercase_vowels():
    assert count_vowels("hello") == 2

def test_uppercase_vowels():
    assert count_vowels("HELLO") == 2

def test_mixed_case():
    assert count_vowels("Hello World") == 3

def test_empty_string():
    assert count_vowels("") == 0

def test_no_vowels():
    assert count_vowels("rhythm") == 0
