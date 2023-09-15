class valueRequiered(Exception):
    def __init__(self, key, message):
        self.key = key
        self.message = message

    def __str__(self):
        return (
            "This value must be sended in request {"
            + self.key
            + ":"
            + self.message
            + "}\n"
        )
