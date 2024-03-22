import re


class StrValidator:
    @staticmethod
    def is_empty_string(value: str) -> bool:
        if value is None or not isinstance(value, str) or value == "":
            return True
        return False

    @staticmethod
    def validate_email_syntax(email):
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if re.match(pattern, email) is None:
            return False
        return True
