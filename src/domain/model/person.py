from collections import namedtuple
from typing import Protocol

from ...utils.custom_date import CustomDate
from ...utils.response_code import ID_NOT_FOUND, INVALID_FORMAT, SCHEMA_NOT_MATCH
from ..DomainError import DomainError
from ..identifier_handler import IdentifierAlgorithm, IdentifierHandler

PersonId = namedtuple("PersonId", ["value"])
Person = namedtuple(
    "Person",
    ["personId", "name", "lastName", "mailAddress", "attrs"],
)
AttrsPerson = namedtuple(
    "AttrsPerson",
    ["birthDate", "documentNumber", "address"],
)


class PersonDomain:
    algorithm = IdentifierAlgorithm.UUID_V4
    pk = "personId"
    fields = Person._fields + AttrsPerson._fields

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
    def as_dict(obj) -> dict:
        return {k: v for k, v in obj._asdict().items() if v is not None}

    @classmethod
    def from_dict(cls, data: list) -> Person | DomainError:
        if data.get(cls.pk, None) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        attr = AttrsPersonDomain.new(data)
        person = {k: v for k, v in data.items() if k in Person._fields}
        person.update({"attrs": attr})

        return Person(**person)

    @classmethod
    def from_repo(cls, data: list) -> Person:
        item = {k: v for k, v in data.items() if k in Person._fields}
        return Person(**item)

    @classmethod
    def new(
        cls,
        identifier: PersonId,
        name: str,
        lastName: str,
        mailAddress: str,
        attrs: AttrsPerson | None,
    ) -> Person | DomainError:
        item = {
            "personId": identifier.value,
            "name": name,
            "lastName": lastName,
            "mailAddress": mailAddress,
            "attrs": attrs.as_dict() if attrs else None,
        }
        return Person(**item)
