from enum import Enum


class BrokerMock:
    queue: str
    data: dict

    @property
    def getDSN(self) -> str:
        pass

    @classmethod
    def setDefault(cls):
        pass

    def send(self, topic: Enum, message: str):
        pass
