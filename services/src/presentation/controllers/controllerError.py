class controllerError(Exception):
    def __init__(self, title, message):
        self.title = title
        self.message = message

    def __str__(self):
        return "---" + self.title + "---\n" + self.message + "\n"
