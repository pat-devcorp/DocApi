from typing import Protocol


class ControllerProtocol(Protocol):
    def __init__(self, writeUId) -> None:
        pass

    def create(self):
        pass

    def fetch(self):
        pass

    def get_by_id(self, identifier):
        pass

    def delete(self, identifier):
        pass

    def update(self, identifier, params: dict):
        pass
