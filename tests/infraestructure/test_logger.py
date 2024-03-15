from src.infrastructure.config import Config
from src.infrastructure.logger.logger import logger_interface_test


def test_logger():
    my_config = Config()
    logger_interface_test(my_config.LOG_CONFIG)
