from collections import namedtuple

from ...utils.custom_date import CustomDate
from ...utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH
from ..DomainError import DomainError
from ..base_domain import BaseDomain
from ..identifier_handler import Identifier, IdentifierHandler, IdentityAlgorithm

Person = namedtuple(
    "Person",
    ["personId", "name", "lastName"],
)
PartialPerson = namedtuple(
    "PartialPerson",
    Person._fields + ["contactIds", "birthDate", "documentNumber", "address"],
)


class PersonDomain(BaseDomain):
    _idAlgorithm = IdentityAlgorithm.UUID_V4
    _pk = "personId"

    @classmethod
    def from_dict(
        cls, identifier: Identifier, data: list
    ) -> Person | PartialPerson | DomainError:
        item = {k: v for k, v in data.items() if k in Person._fields}
        item[cls._pk] = identifier.value

        is_ok, err = cls.is_valid(item)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        if Person._fields != set(item.keys()):
            return PartialPerson(**item)
        return Person(**item)

    @classmethod
    def from_repo(cls, data: list) -> Person | PartialPerson:
        item = {k: v for k, v in data.items() if k in Person._fields}

        if Person._fields != set(item.keys()):
            return PartialPerson(**item)
        return Person(**item)

    @classmethod
    def is_valid(cls, data: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "PersonId": [cls.is_valid_identifier],
            "birthDate": [CustomDate.check_format],
        }

        errors = list()
        for k, v in data.items():
            if is_partial and v is None:
                continue
            if (functions := validate_func.get(k)) is not None:
                for function in functions:
                    is_ok, err = function(v)
                    if not is_ok:
                        errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)
        return True, ""

    @classmethod
    def new(
        cls,
        identifier: Identifier,
        name,
        lastName,
    ) -> Person | DomainError:
        item = {
            "PersonId": identifier.value,
            "name": name,
            "lastName": lastName,
        }

        return Person(**item)
