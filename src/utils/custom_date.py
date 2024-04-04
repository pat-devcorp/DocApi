from datetime import datetime

from ..infrastructure.bootstrap import constant


class BaseDatetime(datetime):
    value: str

    @classmethod
    def not_available(cls):
        date_obj = datetime(1900, 1, 1)
        return date_obj.strftime(cls.str_format)

    @classmethod
    def check_format(cls, value: str | datetime):
        try:
            if isinstance(value, str):
                datetime.strptime(value, cls.str_format)
            elif isinstance(value, datetime):
                formatted_value = value.strftime(cls.str_format)
                if formatted_value != value:
                    raise ValueError("Invalid format")
            else:
                raise ValueError("Invalid type")
            return True, ""
        except ValueError:
            return False, f"{cls.str_format} is not a valid for a date {value}"

    @classmethod
    def now(cls):
        date_obj = datetime.now()
        return cls(date_obj.year, date_obj.month, date_obj.day)

    @classmethod
    def str_now(cls):
        date_obj = datetime.now()
        return date_obj.strftime(cls.str_format)

    @classmethod
    def from_string(cls, date_str):
        date_obj = datetime.strptime(date_str, cls.str_format)
        return cls(date_obj.year, date_obj.month, date_obj.day)

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.value = obj.strftime(cls.str_format)
        return obj


class CustomDate(BaseDatetime):
    str_format = constant.DATE_FORMAT


class CustomDatetime(BaseDatetime):
    str_format = constant.DATE_FORMAT + " " + constant.TIME_FORMAT
