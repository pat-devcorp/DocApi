from typing import Protocol


class UseCaseProtocol(Protocol):
    def fetch(self):
        pass

    def get_by_id(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def create(self):
        pass
