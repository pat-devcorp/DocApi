class ApplicationError(Exception):
    def __init__(self, messages: list):
        self.message = ".\n".join(messages)

    def __str__(self):
        return "--- NOT PRESENT ---\n" + self.message + "-" * 13
