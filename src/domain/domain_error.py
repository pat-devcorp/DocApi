class DomainError(Exception):
    def __init__(self, tittle: str, context_detail: str = ""):
        self.tittle = tittle
        self.context_detail = context_detail

    def __str__(self):
        return self.tittle + "\n" + self.context_detail
