from collections import namedtuple
from typing import TextIO

from ...utils.file_handler import file_exists, upload_file
from ...utils.status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_dict import CustomDict
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..identifier_handler import IdentifierHandler

Image = namedtuple(
    "Image",
    ["image_id", "path", "attrs"],
)


class ImageDomain:
    algorithm = IdentifierAlgorithm.NANO_ID
    pk = "image_id"

    @staticmethod
    def get_invalid_image():
        return Image(
            image_id=0,
            path="/asdasd",
            attrs=list(),
        )

    @classmethod
    def get_valid_image(cls, valid_path, extension_file: str):
        identifier = cls.get_default_identifier(extension_file)
        return Image(
            image_id=identifier.value + extension_file,
            path=valid_path,
            attrs={"mac_address": "60-A5-E2-92-31-73"},
        )

    @classmethod
    def get_default_identifier(cls, extension_file: str) -> IdentifierHandler:
        identifier = IdentifierHandler.get_default_identifier(cls.algorithm)
        identifier.set_value(identifier.value + extension_file)
        return identifier

    @classmethod
    def set_identifier(cls, identifier) -> IdentifierHandler:
        return IdentifierHandler(cls.algorithm, identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, data: list) -> Image | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        item = {k: data.get(k, None) for k in Image._fields}
        attrs = {k: v for k, v in data.items() if k not in Image._fields}
        item["attrs"] = attrs

        cls.is_valid(**item)
        return Image(**item)

    @classmethod
    def is_valid(
        cls,
        image_id,
        path,
        attrs,
    ) -> Image | DomainError:
        errors = list()

        if image_id is not None:
            try:
                cls.set_identifier(image_id)
            except DomainError as e:
                errors.append(str(e))

        if path is not None:
            if not file_exists(path, image_id):
                errors.append(f"Path: {path}  Object: {image_id} is not save to disk")

        if attrs is not None:
            if not CustomDict.has_only_primitive_types(attrs):
                errors.append("the dictionary must have only primitive types")

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        image_file: TextIO,
        image_id: IdentifierHandler,
        path: str,
        attrs: dict = None,
    ) -> Image | DomainError:
        if (
            image_file is None
            or not isinstance(image_id, IdentifierHandler)
            or CustomString.is_empty_string(path)
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        if attrs is None:
            attrs = dict()

        upload_file(path, image_file, image_id.value)

        cls.is_valid(
            image_id.value,
            path,
            attrs,
        )

        return Image(
            image_id.value,
            path,
            attrs,
        )
