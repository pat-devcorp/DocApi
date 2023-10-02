from datetime import datetime

from ...infraestructure.config import Config


def ensureDatetimeFormat(write_at) -> bool:
    try:
        datetime.strftime(write_at, Config.DATETIME_FORMAT)
        return True
    except ValueError:
        return False


def getDatetime() -> str:
    return datetime.strftime(datetime.now(), Config.DATETIME_FORMAT)
