from datetime import datetime

from ...infraestructure.config import Config


def ensureDatetimeFormat(write_at) -> bool:
    try:
        my_config = Config()
        datetime.strftime(write_at, my_config.DATETIME_FORMAT)
        return True
    except ValueError:
        return False


def getDatetime() -> str:
    my_config = Config()
    return datetime.strftime(datetime.now(), my_config.DATETIME_FORMAT)
