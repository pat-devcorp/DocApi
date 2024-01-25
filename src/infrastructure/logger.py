import logging
from logging.handlers import TimedRotatingFileHandler

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


def set_format_to_json(file_path: str):
    formatter = RequestFormatter(
        "{'TIME':%(asctime)s,'ADDRESS':'%(remote_addr)s','URL': '%(url)s','TYPE':'%(levelname)s','MODULE':'%(module)s','MSG':{%(message)s}}"
    )
    handler = TimedRotatingFileHandler(
        file_path, when="midnight", interval=1, encoding="utf8"
    )
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
