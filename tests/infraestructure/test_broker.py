from src.infrastructure.broker.rabbitmq import rabbitmq_interface_test
from src.infrastructure.config import Config


def test_rabbitmq():
    my_config = Config()
    rabbitmq_interface_test(my_config)
