class InterfaceError(Exception):
    def __init__(self, messages: str):
        self.message = messages

    def __str__(self):
        return "--- INTERFACE ---\n" + self.message
