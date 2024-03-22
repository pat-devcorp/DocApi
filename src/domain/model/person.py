from collections import namedtuple

from ...utils.custom_date import CustomDate
from ...utils.response_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..DomainError import DomainError
from ..identifier_handler import IdentifierAlgorithm, IdentifierHandler
from ..str_funcs import StrValidator

PersonId = namedtuple("PersonId", ["value"])
Person = namedtuple(
    "Person",
    [
        "personId",
        "name",
        "lastName",
        "mailAddress",
        "birthDate",
        "documentNumber",
        "address",
    ],
    defaults=[None] * 7,
)


class PersonDomain:
    algorithm = IdentifierAlgorithm.UUID_V4
    pk = "personId"

    @classmethod
    def get_default_identifier(cls):
        return PersonId(IdentifierHandler.get_default_identifier(cls.algorithm))

    @classmethod
    def set_identifier(cls, identifier):
        IdentifierHandler.is_valid(cls.algorithm, identifier)
        return PersonId(identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, data: list) -> Person | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        person = {k: v for k, v in data.items() if k in Person._fields}
        cls.is_valid(person)
        return Person(**person)

    @classmethod
    def is_valid(cls, item: dict) -> None | DomainError:
        data = {k: v for k, v in item.items() if k in Person._fields}
        errors = list()

        if data.get("personId") is not None:
            try:
                cls.set_identifier(data["personId"])
            except DomainError as e:
                errors.append(str(e))

        if data.get("name") is not None:
            if any(character.isdigit() for character in data["name"]):
                errors.append("name contain numbers")

        if data.get("lastName") is not None:
            if any(character.isdigit() for character in data["lastName"]):
                errors.append("lastName contain numbers")

        if data.get("mailAddress") is not None:
            if not StrValidator.validate_email_syntax(data["mailAddress"]):
                errors.append("Invalid email address")

        if data.get("birthDate") is not None:
            is_ok, err = CustomDate.check_format(data["birthDate"])
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        personId: PersonId,
        name: str,
        lastName: str,
        mailAddress: str,
        birthDate=None,
        documentNumber=None,
        address=None,
    ) -> Person | DomainError:
        if (
            personId is None
            or StrValidator.is_empty_string(name)
            or StrValidator.is_empty_string(lastName)
            or StrValidator.is_empty_string(mailAddress)
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")

        item = {
            "personId": personId.value,
            "name": name,
            "lastName": lastName,
            "mailAddress": mailAddress,
        }
        if birthDate is not None:
            item.update({"birthDate": birthDate})
        if documentNumber is not None:
            item.update({"documentNumber": documentNumber})
        if address is not None:
            item.update({"address": address})
        return cls.from_dict(item)
