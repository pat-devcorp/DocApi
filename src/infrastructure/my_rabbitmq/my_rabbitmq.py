import json
import os

import pika
from pydantic import BaseModel

from ...utils.custom_date import CustomDatetime


class RabbitmqServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str


class MyRabbitmqClient:
    def __init__(
        self,
        rabbitmq_server: RabbitmqServer,
        in_lost_save_local: bool = True,
    ) -> None:
        self.server = rabbitmq_server
        self.client = None
        self.channel = None
        self.in_lost_save_local = in_lost_save_local

    def set_queue(self, queue):
        self.queue = queue

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            self.client = None

    @property
    def dsn(self):
        return f"amqp://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}/%2F"

    def _connect(self):
        credentials = pika.PlainCredentials(self.server.username, self.server.password)
        parameters = pika.ConnectionParameters(
            host=self.server.hostname, port=self.server.port, credentials=credentials
        )
        self.client = pika.BlockingConnection(parameters)

        self.channel = self.client.channel()

    def publish(self, message) -> None:
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=message,
        )

    def _saveAsFile(self, message_type, message):
        file_path = "../../tmp/rabbitmq"
        # Ensure the directory structure exists
        os.makedirs(file_path, exist_ok=True)

        now = CustomDatetime.str_now()
        file_name = os.path.join(file_path, +".log")

        with open(file_name, "a+", encoding="utf-8") as f:
            # Check if the file is empty (newly created) and add '['
            f.seek(0, os.SEEK_END)
            if f.tell() == 0:
                f.write("[")
            else:
                # Move the cursor to the end of the file
                f.seek(0, os.SEEK_END)
                # Move one position back to overwrite the trailing ']'
                f.seek(f.tell() - 1, os.SEEK_SET)
                # Add a comma to separate JSON objects
                f.write(",")

            # Dump the JSON data
            json.dump(
                {"type": message_type, "data": message, "write_at": now},
                f,
                ensure_ascii=False,
                indent=4,
            )

            # Add a closing square bracket
            f.write("]")


# Test
def rabbitmq_interface_test(ref_rabbitmq_server):
    rabbitmq_broker = MyRabbitmqClient(ref_rabbitmq_server)
    rabbitmq_broker.set_queue("test")
    rabbitmq_broker.publish("testing...")
