import re


class CustomString:
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

    @staticmethod
    def validate_url_syntax(url):
        regex = r"^(https?|ftp)://[^\s/$.?#].[^\s]*$"
        if re.match(regex, url):
            return True
        else:
            return False
