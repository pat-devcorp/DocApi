class DomainError(Exception):
    def __init__(self, ref_response: tuple[int, str], context_detail: str = ""):
        self.context_detail = context_detail
        self.code, self.response = ref_response

    def __str__(self):
        return str(self.context_detail)
