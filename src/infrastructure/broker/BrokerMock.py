from enum import Enum


class BrokerMock:
    @property
    def chain_connection(self) -> str:
        pass

    @classmethod
    def setToDefault(cls):
        pass

    def sendMessage(self, topic: Enum, message: str):
        pass
