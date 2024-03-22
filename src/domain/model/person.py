from collections import namedtuple
from typing import Protocol

from ...utils.custom_date import CustomDate
from ...utils.response_code import ID_NOT_FOUND, INVALID_FORMAT, SCHEMA_NOT_MATCH
from ..DomainError import DomainError
from ..identifier_handler import IdentifierAlgorithm, IdentifierHandler

PersonId = namedtuple("PersonId", ["value"])
Person = namedtuple(
    "Person",
    ["personId", "name", "lastName", "mailAddress", "birthDate", "documentNumber", "address"],
)


def is_empty_string(value: str) -> bool:
    if value is None or not isinstance(value, str) or value == "":
        return True
    return False

def has_special_char(value: str) -> bool:
    non_alphanumeric_chars = ''
    for char in value:
        if not char.isalnum():
            non_alphanumeric_chars += char
    if non_alphanumeric_chars:
        return True, non_alphanumeric_chars
    return False, ""

def validate_email_syntax(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(pattern, email) is None:
        return False, "Invalid email format""
    return True, ""


class PersonDomain:
    algorithm = IdentifierAlgorithm.UUID_V4
    pk = "personId"
    fields = Person._fields

    @classmethod
    def get_default_identifier(cls):
        identifier = IdentifierHandler(cls.pk, cls.algorithm)
        return PersonId(identifier.get_default_identifier())

    @classmethod
    def set_identifier(cls, identifier):
        identifier = IdentifierHandler(cls.pk, cls.algorithm)
        identifier.is_valid(identifier)
        return PersonId(identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def is_valid(cls, data: dict) -> tuple[bool, str]:
        error = list()

        if data.get("personId") is not None:
            try:
                cls.set_identifier(data["personId"])
            except DomainError as e:
                error.append(e.message)

        if data.get("mailAddress") is not None:
            is_ok, err = cls.validate_email_syntax(data["mailAddress"])
            if not is_ok:
                error.append(err)
        
        if data.get("birthDate") is not None:
            is_ok, err = CustomDate.check_format(data["birthDate"])
            if not is_ok:
                error.append(err)
        
        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))


    @classmethod
    def from_dict(cls, data: list) -> Person | DomainError:
        if data.get(cls.pk, None) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        person = {k: v for k, v in data.items() if k in Person._fields}
        cls.is_valid(person)
        return Person(**person)


    @classmethod
    def new(
        cls,
        identifier: PersonId,
        name: str,
        lastName: str,
        mailAddress: str,
        **kwargs
    ) -> Person | DomainError:
        if identifier is None or is_empty_string(name) or is_empty_string(lastName) or is_empty_string(mailAddress):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        if has_special_char(name) or has_special_char(lastName) or has_special_char(mailAddress):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")

        item = {
            "personId": identifier.value,
            "name": name,
            "lastName": lastName,
            "mailAddress": mailAddress,
        }
        if kwargs:
            item.update(kwargs)
        return cls.from_dict(item)
