class ControllerError(Exception):
    def __init__(self, messages: list):
        self.message = ".\n".join(messages)

    def __str__(self):
        return "--- VALIDATION ---\n" + self.message + "-" * 12
