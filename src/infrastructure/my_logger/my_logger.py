import logging
import threading
from enum import Enum

log_format = (
    "%(levelname)s, "
    '"%(message)s", '
    "%(asctime)s, "
    "%(name)s, "
    "%(module)s, "
    "%(funcName)s, "
    "%(lineno)d, "
    "%(threadName)s"
)


# Define an Enum for log levels
class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def setup_logging(level: LogLevel):
    logger = logging.getLogger(__name__)
    logger.setLevel(level.value)  # Set the logging level

    # Create a file handler and set its format
    log_file = "src/tmp/app.log"  # Path to the log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level.value)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(log_format, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(formatter)

    # Clear any existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Also output logs to console (optional)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger  # Return the logger for use in other functions


def logger_interface_test():
    logger = setup_logging(LogLevel.DEBUG)  # Set up logging with INFO level
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    # Example of logging an exception
    try:
        1 / 0
    except ZeroDivisionError:
        logger.exception("exception message")

    # Demonstrating thread logging
    def threaded_function():
        logger.debug("message from a thread")

    thread = threading.Thread(target=threaded_function, name="MyThread")
    thread.start()
    thread.join()
