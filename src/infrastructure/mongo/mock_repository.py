class MockRepositoryClient:
    def __init__(self, data) -> None:
        self.object = data

    def dsn(self):
        return "mock-repos"

    def fetch(self, attrs, matching):
        return [self.object]

    def get_by_id(self, identifier, attrs):
        return self.object

    def delete(self, identifier) -> None:
        return None

    def update(self, identifier, kwargs) -> None:
        return None
