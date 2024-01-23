from enum import Enum


class MockBroker:
    queue: str
    data: dict

    @property
    def getDSN(self) -> str:
        pass

    @classmethod
    def setDefault(cls):
        pass

    def publish(self, topic: Enum, message: str):
        pass
