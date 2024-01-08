from datetime import datetime

from ..infrastructure.config import Config


def hasValidFormat(obj_date, format) -> bool:
    try:
        datetime.strptime(obj_date, format)
        return True
    except ValueError:
        return False


def checkDatetimeFormat(obj_date) -> bool:
    my_config = Config()
    return hasValidFormat(obj_date, my_config.DATETIME_FORMAT)


def checkDateFormat(obj_date) -> bool:
    my_config = Config()
    return hasValidFormat(obj_date, my_config.DATE_FORMAT)


def getDatetime() -> str:
    my_config = Config()
    current_datetime = datetime.now()
    return current_datetime.strftime(my_config.DATETIME_FORMAT)
