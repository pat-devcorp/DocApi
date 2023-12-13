import json
import re

from kafka import KafkaProducer

from ...application.BrokerTopic import BrokerTopic
from ...utils.ResponseHandler import BROKER_CONNECTION_FAIL, BROKER_SEND_FAIL
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
        except Exception:
            raise InfraestructureError(BROKER_CONNECTION_FAIL)

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

        except Exception:
            raise InfraestructureError(BROKER_SEND_FAIL)

    def consumeMessage(self, topic: str):
        try:
            return self.consumer(topic)
        except Exception:
            raise InfraestructureError(BROKER_SEND_FAIL)
