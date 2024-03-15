from datetime import datetime


def has_valid_format(obj_date, format) -> bool:
    try:
        datetime.strptime(obj_date, format)
        return True
    except ValueError:
        return False


class CustomDate(datetime):
    value: str
    date_format = "%Y-%m-%d"

    @classmethod
    def check_format(value):
        return has_valid_format(value, cls.date_format)

    @classmethod
    def now(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def from_string(cls, date_str):
        dt_obj = datetime.strptime(date_str, cls.date_format)
        return cls(
            dt_obj.year,
            dt_obj.month,
            dt_obj.day
        )

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.value = obj.strftime(cls.date_format)
        return obj


class CustomDatetime(datetime):
    value: str
    datetime_format = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def check_format(value):
        return has_valid_format(value, cls.datetime_format)

    @classmethod
    def now(cls):
        dt_obj = datetime.now()
        return cls(dt_obj.year, dt_obj.month, dt_obj.day)

    @classmethod
    def from_string(cls, date_str):
        dt_obj = datetime.strptime(date_str, cls.datetime_format)
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
