from enum import Enum


class MockBroker:
    queue: str
    data: dict

    @property
    def dsn(self) -> str:
        pass

    @classmethod
    def set_default(cls, config):
        pass

    def publish(self, topic: Enum, message: str):
        pass
