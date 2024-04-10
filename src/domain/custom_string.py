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

    @staticmethod
    def sanitize_string(text):
        """
        Sanitizes a string by removing potentially harmful characters.

        Args:
            text: The string to sanitize.

        Returns:
            The sanitized string.
        """
        # Common SQL injection keywords (case-insensitive)
        injection_pattern = (
            r"(union|select|insert|update|delete|drop|or|and|\*|\')|\b(exec|execute)\b"
        )

        # Sanitize using regular expressions
        return re.sub(injection_pattern, "", text, flags=re.IGNORECASE)

    @staticmethod
    def check_suspicious_keywords(text):
        """
        Performs basic checks for common NoSQL injection keywords.

        **Note:** This is not a robust method and should be used with caution.

        Args:
            text: The string to check.

        Returns:
            True if suspicious patterns are found, False otherwise.
        """
        injection_keywords = ["$", "or", "and", "--", ";"]
        for keyword in injection_keywords:
            if keyword.lower() in text.lower():
                return True
        return False
