from datetime import datetime


def has_valid_format(obj_date, format) -> bool:
    try:
        datetime.strptime(obj_date, format)
        return True
    except ValueError:
        return False


class BaseDatetime(datetime):
    value: str

    @classmethod
    def check_format(cls, value):
        return has_valid_format(value, cls.str_format)

    @classmethod
    def now(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def str_now(cls):
        dt_obj = datetime.now()
        return dt_obj.strftime(cls.str_format)

    @classmethod
    def from_string(cls, date_str):
        dt_obj = datetime.strptime(date_str, cls.str_format)
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.value = obj.strftime(cls.str_format)
        return obj


class CustomDate(BaseDatetime):
    str_format = "%Y-%m-%d"


class CustomDatetime(BaseDatetime):
    str_format = "%Y-%m-%d %H:%M:%S"
