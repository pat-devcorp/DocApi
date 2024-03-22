import json
import os

import pika
from pydantic import BaseModel

from ...utils.custom_date import CustomDatetime
from ...utils.response_code import (
    BROKER_CHANNEL_ERROR,
    BROKER_CONNECTION_FAIL,
    BROKER_SEND_FAIL,
)
from ..InfrastructureError import InfrastructureError


class RabbitmqServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    queue_name: str
    lost_message_path: str


class RabbitmqClient:
    def __init__(
        self,
        rabbitmq_server: RabbitmqServer,
        queue: str,
        in_lost_save_local: bool = True,
    ) -> None:
        self.server = rabbitmq_server
        self.queue = queue
        self.client = None
        self.channel = None
        self.in_lost_save_local = in_lost_save_local

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

    def publish(self, message) -> None | InfrastructureError:
        try:
            self._connect()
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                body=message,
            )
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
        file_path = os.path.join(self.server.lost_message_path, self.queue)
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
                {"type": message_type, "data": message, "writeAt": now},
                f,
                ensure_ascii=False,
                indent=4,
            )

            # Add a closing square bracket
            f.write("]")


# Test
def rabbitmq_interface_test(ref_rabbitmq_server):
    rabbitmq_broker = RabbitmqClient(ref_rabbitmq_server, "test")
    rabbitmq_broker.publish("testing...")
