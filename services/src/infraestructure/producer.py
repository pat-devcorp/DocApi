import json

from kafka import KafkaProducer


class Producer:
    def __init__(self, host: str, port: int):
        self.bootstrap_servers = host + ":" + str(port)
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )

    def send_message(self, topic, message_dict):
        try:
            # Send the message to the specified topic
            self.producer.send(topic, value=message_dict)
            self.producer.flush()
            print(f"Message sent to topic '{topic}': {message_dict}")

        except Exception as e:
            print(f"Error sending message to Kafka: {str(e)}")
