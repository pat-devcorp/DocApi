import json
import re
from enum import Enum

from kafka import KafkaConsumer, KafkaProducer

from ...application.BrokerTopic import BrokerTopic
from ..config import Config
from ..InfraestructureError import InfraestructureError


class Kafka:
    host: str
    port: int

    def __init__(self, host: str = None, port: int = None):
        self.host = host
        self.port = port
        my_config = Config()
        self.prefix = my_config.KAFKA_PREFIX

    @property
    def chain_connection(self):
        return self.host + ":" + str(self.port)

    @classmethod
    def setToDefault(cls):
        my_config = Config()
        return cls(my_config.KAFKA_HOST, my_config.KAFKA_PORT)

    def startConnection(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.chain_connection,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except Exception as e:
            raise InfraestructureError(f"Failed to connect to Kafka {str(e)}")

    def sendMessage(self, topic: BrokerTopic, message: str):
        self.startConnection()
        pattern = r"\b\w+:\d+\.\d+\.\d+\.\d+\/"
        if re.match(pattern, message):
            raise InfraestructureError("Pattern '{pattern}' not found in {message}")
        try:
            topic = self.prefix + "/" + topic.value
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic '{topic.value}': {message}")

        except Exception as e:
            raise InfraestructureError(f"Error sending message to Kafka: {str(e)}")

    def consumeMessage(self, topic: str):
        try:
            return self.consumer(topic)
        except Exception as e:
            raise InfraestructureError(f"Error sending message to Kafka: {str(e)}")
