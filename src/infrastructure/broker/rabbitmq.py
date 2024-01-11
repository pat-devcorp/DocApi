import functools
import json

import pika
from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress

from infrastructure.config import Config

from ...utils.ResponseHandler import (
    BROKER_CHANNEL_ERROR,
    BROKER_CONNECTION_FAIL,
    BROKER_SEND_FAIL,
)
from ..InfrastructureError import InfrastructureError


class RabbitmqServer(BaseModel):
    server: IPvAnyAddress
    port: int
    user: str
    password: str
    queue_name: str
    exchange_name: str
    exchange_type: str


class PikaPublisher:
    def __init__(self, rabbitmq_dto: RabbitmqServer):
        self.rabbitmq_dto = rabbitmq_dto
        self.client = None
        self._channel = None

    @classmethod
    def setDefault(cls, queue_name):
        my_config = Config()
        con = RabbitmqServer(
            server=my_config.RABBITMQ_HOST,
            port=my_config.RABBITMQ_PORT,
            user=my_config.RABBITMQ_USER,
            password=my_config.RABBITMQ_PASSWORD,
            queue_name=queue_name,
            exchange_name="message_exchange",
            exchange_type="direct",
        )
        return cls(con)

    def startConnection(self):
        try:
            credentials = pika.PlainCredentials(
                self.rabbitmq_dto.user, self.rabbitmq_dto.password
            )
            self.client = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.rabbitmq_dto.server,
                    port=self.rabbitmq_dto.port,
                    credentials=credentials,
                )
            )
        except Exception as err:
            raise InfrastructureError(BROKER_CONNECTION_FAIL, str(err))

    def _setChannel(self):
        if not self.client or self.client.is_closed:
            self._start_connection()
        try:
            self._channel = self.client.channel()
            self._channel.exchange_declare(
                exchange=self.exchange_name, exchange_type=self.exchange_type
            )
        except Exception as err:
            raise InfrastructureError(BROKER_CHANNEL_ERROR, str(err))

    def manage_connection(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not self._channel or self._channel.is_closed:
                self._setChannel()
            try:
                return func(self, *args, **kwargs)
            finally:
                # Close connection only when necessary (e.g., when encountering errors)
                if self.client and not self.client.is_closed:
                    self.client.close()

        return wrapper

    @manage_connection
    def send_message(self, message_type, message):
        try:
            message = json.dumps({"type": message_type, "message": message})
            self._channel.basic_publish(
                exchange=self.rabbitmq_dto.message_exchange,
                routing_key=self.rabbitmq_dto.queue_name,
                body=message,
            )
        except Exception as err:
            raise InfrastructureError(BROKER_SEND_FAIL, str(err))
