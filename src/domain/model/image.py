from collections import namedtuple

from ...utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH
from ..DomainError import DomainError
from ..identifier_handler import Identifier, IdentifierHandler, IdentityAlgorithm

Image = namedtuple(
    "Image",
    ["imageId", "url"],
)


class ImageDomain:
    _idAlgorithm = IdentityAlgorithm.UUID_V4
    _pk = "ImageId"

    @classmethod
    def get_identifier(cls) -> Identifier:
        identifier = IdentifierHandler.get_default(cls._idAlgorithm)
        return Identifier(identifier, cls._idAlgorithm, cls._pk)

    @classmethod
    def is_valid_identifier(cls, identifier) -> None | DomainError:
        is_ok, err = IdentifierHandler.is_valid(identifier, cls._idAlgorithm)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)

    @classmethod
    def set_identifier(cls, identifier) -> Identifier | DomainError:
        cls.is_valid_identifier(identifier)
        return Identifier(identifier, cls._idAlgorithm, cls._pk)

    @staticmethod
    def as_dict(Image: Image) -> dict:
        return {k: v for k, v in Image._asdict().items() if k is not None}

    @classmethod
    def from_dict(cls, identifier: Identifier, data: list) -> Image | DomainError:
        item = {k: v for k, v in data.items() if k in Image._fields}
        item[cls._pk] = identifier.value

        is_ok, err = cls.is_valid(item)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        return Image(**item)

    @classmethod
    def from_repo(cls, data: list) -> Image:
        item = {k: v for k, v in data.items() if k in Image._fields}
        return Image(**item)

    @classmethod
    def is_valid(cls, data: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {"ImageId": [cls.is_valid_identifier]}

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
    ) -> Image | DomainError:
        item = {"ImageId": identifier.value, "name": name}

        return Image(**item)
