from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.rabbitmq import rabbitmq_interface_test


def test_rabbitmq():
    my_config = Bootstrap()
    rabbitmq_interface_test(my_config.RABBITMQ_SERVER)
