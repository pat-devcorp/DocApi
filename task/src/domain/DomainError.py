class DomainError(Exception):
    def __init__(self, messages: list):
        self.message = ".\n".join(messages)

    def __str__(self):
        return "--- STRUCT DOES NOT MATCH ---\n" + self.message
