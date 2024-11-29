from ..domain.identifier_handler import IdentifierHandler
from ..domain.model.constant import INVALID_FORMAT, WRITER_NOT_FOUND
from ..utils.custom_date import CustomDatetime
from ..utils.handler_error import HandlerError
from .application_error import ApplicationError


class AuditHandler:
    _fields = ["writeUId", "writeAt", "createUId", "createAt", "isFromRepo"]

    @classmethod
    def is_valid(
        cls,
        writeUId,
        writeAt,
        createUId,
        createAt,
        isFromRepo
    ) -> list:
        errors = list()

        if writeUId is None:
            errors.append("Write user is required")

        if writeAt is None:
            is_ok, err = CustomDatetime.check_format(writeAt)
            if not is_ok:
                errors.append(err)

        if createAt is not None:
            is_ok, err = CustomDatetime.check_format(createAt)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise ApplicationError(INVALID_FORMAT, "\n".join(errors))

        return {
            "writeUId": writeUId,
            "writeAt": writeAt,
            "createUId": createUId,
            "createAt": createAt,
        }

    @classmethod
    def from_dict(cls, data: dict) -> dict | HandlerError:
        writeUId = data.get("writeUId")
        if writeUId is None:
            raise HandlerError(WRITER_NOT_FOUND)

        item = dict()
        for k in cls._fields:
            item[k] = data.get(k, None)

        return cls.is_valid(**item)

    @classmethod
    def get_update_fields(cls, currentUId: str) -> dict:
        return {"writeUId": currentUId, "writeAt": CustomDatetime.str_now()}

    @classmethod
    def get_create_fields(cls, currentUId: str) -> dict:
        now = CustomDatetime.str_now()
        return cls.is_valid(
            currentUId,
            now,
            currentUId,
            now,
            false
        )
