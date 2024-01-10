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

class DateHandler(datetime):
    value: str


    @classmethod
    def getDefault(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def fromStr(cls, date_str):
        my_config = Config()
        dt_obj = datetime.strptime(date_str, my_config.DATE_FORMAT)
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)


    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        my_config = Config()
        obj.value = obj.strftime(my_config.DATE_FORMAT)
        return obj


class DateTimeHandler(datetime):
    value: str


    @classmethod
    def getDefault(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)


    @classmethod
    def fromStr(cls, date_str):
        my_config = Config()
        dt_obj = datetime.strptime(date_str, my_config.DATETIME_FORMAT)
        return cls(dt_obj.year, dt_obj.month, dt_obj.day, dt_obj.hour, dt_obj.minute, dt_obj.second)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        my_config = Config()
        obj.value = obj.strftime(my_config.DATETIME_FORMAT)
        return obj