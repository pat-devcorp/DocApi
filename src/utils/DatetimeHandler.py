from datetime import datetime

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def hasValidFormat(obj_date, format) -> bool:
    try:
        datetime.strptime(obj_date, format)
        return True
    except ValueError:
        return False


def check_datetime_format(obj_date, datetime_format=DATETIME_FORMAT) -> bool:
    return hasValidFormat(obj_date, datetime_format)


def checkDateFormat(obj_date, date_format=DATE_FORMAT) -> bool:
    return hasValidFormat(obj_date, date_format)


def get_datetime(datetime_format=DATETIME_FORMAT) -> str:
    current_datetime = datetime.now()
    return current_datetime.strftime(datetime_format)


class DateHandler(datetime):
    value: str

    @classmethod
    def now(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def from_string(cls, date_str, date_format=DATE_FORMAT):
        dt_obj = datetime.strptime(date_str, date_format)
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.value = obj.strftime(DATE_FORMAT)
        return obj


class DateTimeHandler(datetime):
    value: str

    @classmethod
    def now(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def from_string(cls, date_str, datetime_format=DATETIME_FORMAT):
        dt_obj = datetime.strptime(date_str, datetime_format)
        return cls(
            dt_obj.year,
            dt_obj.month,
            dt_obj.day,
            dt_obj.hour,
            dt_obj.minute,
            dt_obj.second,
        )

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.value = obj.strftime(DATETIME_FORMAT)
        return obj
