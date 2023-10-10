import json
import re

from kafka import KafkaProducer

from .config import Config
from .InfraestructureError import InfraestructureError


class Producer:
    host: str
    port: int

    def __init__(self, host: str = None, port: int = None):
        self.host = host
        self.port = port

    def startConnection(self):
        try:
            self.bootstrap_servers = self.host + ":" + str(self.port)
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except Exception as e:
            raise InfraestructureError(f"Failed to connect to Kafka {str(e)}")

    @classmethod
    def setToDefault(cls):
        my_config = Config()
        return cls(my_config.PRODUCER_HOST, my_config.PRODUCER_PORT)

    def send_message(self, topic: str, message: str):
        self.startConnection()
        pattern = r"[a-zA-Z0-9\._\-]+"
        if not re.match(pattern, message):
            raise InfraestructureError("Pattern '{pattern}' not found in {message}")
        try:
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic '{topic}': {message}")

        except Exception as e:
            raise InfraestructureError(f"Error sending message to Kafka: {str(e)}")
