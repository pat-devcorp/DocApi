from infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.logger.logger import logger_interface_test


def test_logger():
    my_config = Bootstrap()
    logger_interface_test(my_config.LOG_CONFIG)
