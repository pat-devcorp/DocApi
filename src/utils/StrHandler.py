import re

from validator_collection.checkers import is_not_empty


def containsOnlyLetters(input_string):
    # Use a regular expression to check for only letters (uppercase or lowercase)
    return re.match("^[a-zA-Z]*$", input_string) is not None


def valMaxLength(text, size):
    return is_not_empty(text, max_length=size)
