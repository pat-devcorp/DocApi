import json
import os
from typing import Protocol

import pika
from pydantic import BaseModel

from ...utils.datetime_handler import get_datetime
from ...utils.ResponseHandler import (
    BROKER_CHANNEL_ERROR,
    BROKER_CONNECTION_FAIL,
    BROKER_SEND_FAIL,
)
from ..InfrastructureError import InfrastructureError


class RabbitmqConfig(Protocol):
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    BROKER_LOST_MESSAGE_PATH: str


class RabbitmqServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    queue_name: str
    lost_message_path: str


class Rabbitmq:
    def __init__(
        self, rabbitmq_server: RabbitmqServer, in_lost_save_local: bool = True
    ):
        self.server = rabbitmq_server
        self.client = None
        self.channel = None
        self.in_lost_save_local = in_lost_save_local

    @property
    def dsn(self):
        return f"amqp://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}/%2F"

    @classmethod
    def set_default(cls, my_config: RabbitmqConfig, queue_name: str):
        con = RabbitmqServer(
            hostname=my_config.RABBITMQ_HOST,
            port=my_config.RABBITMQ_PORT,
            username=my_config.RABBITMQ_USER,
            password=my_config.RABBITMQ_PASS,
            lost_message_path=my_config.BROKER_LOST_MESSAGE_PATH,
            queue_name=queue_name,
        )
        return cls(con)

    def _connect(self):
        credentials = pika.PlainCredentials(self.server.username, self.server.password)
        parameters = pika.ConnectionParameters(
            host=self.server.hostname, port=self.server.port, credentials=credentials
        )
        self.client = pika.BlockingConnection(parameters)

        self.channel = self.client.channel()

    def publish(self, message):
        try:
            self._connect()
            self.channel.basic_publish(
                exchange="",
                routing_key=self.server.queue_name,
                body=message,
            )
            print(f"Message sent to queue: {self.server.queue_name}")
        except pika.exceptions.AMQPConnectionError:
            raise InfrastructureError(
                BROKER_CONNECTION_FAIL, "Connection to RabbitMQ failed"
            )
        except pika.exceptions.ChannelClosed:
            raise InfrastructureError(BROKER_CHANNEL_ERROR, "Channel is closed")
        except Exception as e:
            self._saveAsFile("json", str(e))
            raise InfrastructureError(BROKER_SEND_FAIL, str(e))
        finally:
            if self.client:
                self.client.close()

    def _saveAsFile(self, message_type, message):
        file_path = os.path.join(self.server.lost_message_path, self.server.queue_name)
        # Ensure the directory structure exists
        os.makedirs(file_path, exist_ok=True)

        file_name = os.path.join(file_path, get_datetime() + ".log")

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
                {"type": message_type, "data": message, "writeAt": get_datetime()},
                f,
                ensure_ascii=False,
                indent=4,
            )

            # Add a closing square bracket
            f.write("]")


# Test
def rabbitmq_interface_test(my_config):
    rabbitmq_broker = Rabbitmq.set_default(my_config, "test")
    rabbitmq_broker.publish("testing...")
