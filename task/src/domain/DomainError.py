from ..utils.ErrorHandler import ResponseDTO


class DomainError(Exception):
    def __init__(self, message, ref_response: ResponseDTO):
        self. message = message
        self.response = ref_response

    def __str__(self):
        return str(self.response)
