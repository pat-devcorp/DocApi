import json
import re
from typing import Protocol

from kafka import KafkaProducer

from ...application.BrokerTopic import BrokerTopic
from ...utils.response_code import BROKER_CONNECTION_FAIL, BROKER_SEND_FAIL
from ..InfrastructureError import InfrastructureError


class KafkaConfig(Protocol):
    KAFKA_HOST: str
    KAFKA_PORT: int
    KAFKA_PREFIX: str


class KafkaBroker:
    host: str
    port: int

    def __init__(self, host: str, port: int, prefix: str):
        self.host = host
        self.port = port
        self.prefix = prefix

    @property
    def dsn(self):
        return self.host + ":" + str(self.port)

    @classmethod
    def set_default(cls, my_config: KafkaConfig):
        return cls(my_config.KAFKA_HOST, my_config.KAFKA_PORT, my_config.KAFKA_PREFIX)

    def startConnection(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.dsn,
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
#     kafka_producer = Kafka.set_default()
#     assert kafka_producer.dsn == "172.25.0.2:9092"
#     current_id = "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"

#     dto = {
#         "write_uid": "8888",
#         "_id": current_id,
#         "description": "This is a ticket modified",
#     }
#     try:
#         kafka_producer.send("create/task", str(dto))
#         assert True
#     except Exception as e:
#         assert False
