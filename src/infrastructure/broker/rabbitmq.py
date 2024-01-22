import json
import os

import pika
from pydantic import BaseModel

from ...infrastructure.config import Config
from ...utils.DatetimeHandler import getDatetime

from ...utils.ResponseHandler import (
    BROKER_SEND_FAIL,
)
from ..InfrastructureError import InfrastructureError


def rabbitmqTestingInterface():
    rabbitmq_broker = Rabbitmq.setDefault("test")
    rabbitmq_broker.send_message("testing...")


class RabbitmqServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    queue_name: str
    exchange_name: str
    exchange_type: str


class Rabbitmq:
    def __init__(
        self, rabbitmq_server: RabbitmqServer, in_lost_save_local: bool = True
    ):
        self.server = rabbitmq_server
        self.client = None
        self.channel = None
        self.in_lost_save_local = in_lost_save_local

    @property
    def getDSN(self):
        return f"amqp://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}/%2F"

    def _saveAsFile(self, message_type, message):
        my_config = Config()
        file_path = os.path.join(my_config.BROKER_LOST_MESSAGE_PATH, self.server.queue_name)
        # Ensure the directory structure exists
        os.makedirs(file_path, exist_ok=True)

        file_name = os.path.join(file_path, getDatetime() + ".log")

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
                {"type": message_type, "data": message, "writeAt": getDatetime()},
                f,
                ensure_ascii=False,
                indent=4,
            )

            # Add a closing square bracket
            f.write("]")

    def __enter__(self):
        print("CONNECTING")
        credentials = pika.PlainCredentials(self.server.username, self.server.password)
        parameters = pika.ConnectionParameters(host=self.server.hostname, port=self.server.port, credentials=credentials)
        self.client = pika.BlockingConnection(parameters)

        self.channel = self.client.channel()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("EXIT")
        if self.client:
            self.client.close()


    @classmethod
    def setDefault(cls, queue_name):
        my_config = Config()
        con = RabbitmqServer(
            hostname=my_config.RABBITMQ_HOST,
            port=my_config.RABBITMQ_PORT,
            username=my_config.RABBITMQ_USER,
            password=my_config.RABBITMQ_PASS,
            queue_name=queue_name,
            exchange_name="message_exchange",
            exchange_type="direct",
        )
        return cls(con)

    def send_message(self, message):
        print("SENDING...")
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.server.queue_name,
                body=message,
            )
            print(f"Message sent to queue: {self.server.queue_name}")
        except pika.exceptions.AMQPConnectionError:
            print("Connection to RabbitMQ failed")
        except pika.exceptions.ChannelClosed:
            print("Channel is closed")
        except Exception as e:
            print(f"Unexpected error: {e}")
