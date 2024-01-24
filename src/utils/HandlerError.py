class HandlerError(Exception):
    def __init__(self, ref_response: tuple, context_detail=""):
        self.context_detail = context_detail
        self.code, self.response = ref_response

    def __str__(self):
        return str(self.response[1])
