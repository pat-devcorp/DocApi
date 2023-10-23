from datetime import datetime

from ..infraestructure.config import Config


def valdiateDatetimeFormat(write_at) -> bool:
    try:
        my_config = Config()
        datetime.strptime(write_at, my_config.DATETIME_FORMAT)
        return True
    except ValueError:
        return False

def getDatetime() -> str:
    my_config = Config()
    current_datetime = datetime.now()
    return current_datetime.strftime(my_config.DATETIME_FORMAT)
