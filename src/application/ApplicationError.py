class ApplicationError(Exception):
    def __init__(self, ref_response: tuple, detail=""):
        self.detail = detail
        self.code, self.response = ref_response

    def __str__(self):
        return str(self.response)
