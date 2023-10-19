from ...application.ProducerTopic import ProducerTopic

class BrokerMock:
    @property
    def chain_connection(self) -> str:
        pass
    
    @classmethod
    def setToDefault(cls):
        pass
    
    def sendMessage(self, topic: ProducerTopic, message: str):
        pass