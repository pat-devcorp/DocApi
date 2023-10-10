class InfraestructureError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "--- INFRAESTRUCTURE ---\n" + self.message + "\n"
