class MockRepository:
    _name: str
    _pk: str
    _fields: list

    def entityExists(self, identifier):
        return dict()

    def fetch(self) -> list:
        return list()

    def getById(self, identity) -> list:
        return dict()

    def delete(self, identity) -> bool:
        return True

    def create(self, data) -> bool:
        return True

    def update(self, data) -> bool:
        return True
