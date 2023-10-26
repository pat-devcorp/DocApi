import re


def contains_only_letters(input_string):
    # Use a regular expression to check for only letters (uppercase or lowercase)
    return re.match("^[a-zA-Z]*$", input_string) is not None
