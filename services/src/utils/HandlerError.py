class HandlerError(Exception):
    def __init__(self, messages):
        self.message = messages

    def __str__(self):
        return "--- HANDLER ---\n" + self.message + "-" * 12
