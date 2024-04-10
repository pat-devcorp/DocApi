from ..domain.identifier_handler import IdentifierHandler
from ..utils.custom_date import CustomDatetime
from ..utils.HandlerError import HandlerError
from ..utils.status_code import INVALID_FORMAT, WRITER_NOT_FOUND
from .ApplicationError import ApplicationError


class AuditHandler:
    _fields = ["write_uid", "write_at", "create_uid", "create_at"]

    @classmethod
    def is_valid(
        cls,
        write_uid,
        write_at,
        create_uid,
        create_at,
    ) -> list:
        errors = list()

        if write_uid is None:
            errors.append("Write user is required")

        if write_at is None:
            is_ok, err = CustomDatetime.check_format(write_at)
            if not is_ok:
                errors.append(err)

        if create_at is not None:
            is_ok, err = CustomDatetime.check_format(create_at)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise ApplicationError(INVALID_FORMAT, "\n".join(errors))

        return {
            "write_uid": write_uid,
            "write_at": write_at,
            "create_uid": create_uid,
            "create_at": create_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> dict | HandlerError:
        write_uid = data.get("write_uid")
        if write_uid is None:
            raise HandlerError(WRITER_NOT_FOUND)

        item = dict()
        for k in cls._fields:
            item[k] = data.get(k, None)

        return cls.is_valid(**item)

    @classmethod
    def get_update_fields(cls, identifier: IdentifierHandler) -> dict | HandlerError:
        current_uid = identifier.value
        return {"write_uid": current_uid, "write_at": CustomDatetime.str_now()}

    @classmethod
    def get_create_fields(cls, identifier: IdentifierHandler) -> dict | HandlerError:
        now = CustomDatetime.str_now()
        current_uid = identifier.value
        return cls.is_valid(
            current_uid,
            now,
            current_uid,
            now,
        )
