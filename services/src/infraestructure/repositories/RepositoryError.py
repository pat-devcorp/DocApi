class RepositoryError(Exception):
    def __init__(self, title, message):
        self.title = title
        self.message = message

    def __str__(self):
        return "--- REPOSITORY ---\n" + self.message + "\n"
