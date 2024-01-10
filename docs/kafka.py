import json
import re

from kafka import KafkaProducer

from ...application.BrokerTopic import BrokerTopic
from ...utils.ResponseHandler import BROKER_CONNECTION_FAIL, BROKER_SEND_FAIL
from ..config import Config
from ..InfrastructureError import InfrastructureError


class KafkaBroker:
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
            raise InfrastructureError(BROKER_CONNECTION_FAIL)

    def publish(self, topic: BrokerTopic, message: str):
        self.startConnection()
        pattern = r"\b\w+:\d+\.\d+\.\d+\.\d+\/"
        if re.match(pattern, message):
            raise InfrastructureError("Pattern '{pattern}' not found in {message}")
        try:
            topic = self.prefix + "/" + topic.value
            self.producer.send(topic, value=message)
            self.producer.flush()
            print(f"Message sent to topic '{topic.value}': {message}")

        except Exception:
            raise InfrastructureError(BROKER_SEND_FAIL)

    def consume(self, topic: str):
        try:
            return self.consumer(topic)
        except Exception:
            raise InfrastructureError(BROKER_SEND_FAIL)

# def test_kafka_producer():
#     print("----KAFKA PROD")
#     kafka_producer = Kafka.setToDefault()
#     assert kafka_producer.chain_connection == "172.25.0.2:9092"
#     current_id = "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"

#     dto = {
#         "writeUId": "8888",
#         "_id": current_id,
#         "description": "This is a ticket modified",
#     }
#     try:
#         kafka_producer.sendMessage("create/task", str(dto))
#         assert True
#     except Exception as e:
#         assert False
