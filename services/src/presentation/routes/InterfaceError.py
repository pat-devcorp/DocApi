class InterfaceError(Exception):
    def __init__(self, messages: list):
        self.message = ".\n".join(messages)

    def __str__(self):
        return "--- ARGS REQUIRED ---\n" + self.message + "-" * 21
