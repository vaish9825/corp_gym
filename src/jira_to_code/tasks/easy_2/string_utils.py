def count_vowels(text):
    """Count the number of vowels (a, e, i, o, u) in the given text.
    Should be case-insensitive.
    """
    # BUG: Only counts lowercase vowels, ignores uppercase
    count = 0
    for char in text:
        if char in 'aeiou':
            count += 1
    return count
