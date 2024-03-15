from enum import Enum


class CustomEnum(Enum):
    @classmethod
    def has_value(cls, value):
        if not any(value == item.value for item in cls):
            return False, f"{value} is not member"
        return True, ""
