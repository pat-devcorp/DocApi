class RepositoryMock:
    def __init__(self, identifier, dao_mock):
        self.identity = identifier
        self.data = dao_mock

    def entityExists(self, identifier):
        return None

    def fetch(self) -> list:
        return [self.data]

    def getByID(self, identity) -> list:
        return self.data

    def delete(self, identity) -> bool:
        return True

    def create(self, data) -> bool:
        return True

    def update(self, data) -> bool:
        return True
