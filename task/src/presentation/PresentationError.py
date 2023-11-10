class PresentationError(Exception):
    def __init__(self, messages: list):
        self.message = messages

    def __str__(self):
        return "--- PRESENTATION ---\n" + self.message
