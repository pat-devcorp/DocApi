from ...application.BrokerTopic import BrokerTopic


class BrokerMock:
    @property
    def chain_connection(self) -> str:
        pass

    @classmethod
    def setToDefault(cls):
        pass

    def sendMessage(self, topic: BrokerTopic, message: str):
        pass
