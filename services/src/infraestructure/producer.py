import json
from kafka import KafkaProducer

from .config import Config


class Producer:
    host:str
    port: int

    def __init__(self, host: str=None, port: int=None):
        if host is None:
            self.setToDefaultServer()
        else:
            self.host = host
            self.port = port
        self.bootstrap_servers = self.host + ":" + str(self.port)
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def setToDefaultServer(self):
        my_config = Config()
        self.host = my_config.PRODUCER_HOST
        self.port = my_config.PRODUCER_PORT

    def send_message(self, topic: str, message: str):
        try:
            # Send the message to the specified topic
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic '{topic}': {message}")

        except Exception as e:
            print(f"Error sending message to Kafka: {str(e)}")
