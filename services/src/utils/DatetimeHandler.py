from datetime import datetime

from ..infraestructure.config import Config


class DateTimeHandler:
    @staticmethod
    def valdiateDatetimeFormat(write_at) -> bool:
        try:
            my_config = Config()
            datetime.strptime(write_at, my_config.DATETIME_FORMAT)
            return True
        except ValueError:
            return False

    @staticmethod
    def getDatetime() -> str:
        my_config = Config()
        current_datetime = datetime.now()
        return current_datetime.strftime(my_config.DATETIME_FORMAT)
