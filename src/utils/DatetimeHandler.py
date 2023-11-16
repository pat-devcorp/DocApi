from datetime import datetime

from ..infraestructure.config import Config


def valdiateFormat(obj_date, format) -> bool:
    try:
        datetime.strptime(obj_date, format)
        return True
    except ValueError:
        return False


def valdiateDatetimeFormat(obj_date) -> bool:
    my_config = Config()
    return valdiateFormat(obj_date, my_config.DATETIME_FORMAT)


def valdiateDateFormat(obj_date) -> bool:
    my_config = Config()
    return valdiateFormat(obj_date, my_config.DATE_FORMAT)


def getDatetime() -> str:
    my_config = Config()
    current_datetime = datetime.now()
    return current_datetime.strftime(my_config.DATETIME_FORMAT)
