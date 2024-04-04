from collections import namedtuple

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

    @classmethod
    def get_default_identifier(cls) -> IdentifierHandler:
        return IdentifierHandler.get_default_identifier(cls.algorithm)

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
        image_file,
        image_id: IdentifierHandler,
        path: str,
        attrs: dict = None,
    ) -> Image | DomainError:
        if not isinstance(image_id, IdentifierHandler) or CustomString.is_empty_string(
            path
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        if attrs is None:
            attrs = dict()

        identifier = upload_file(path, image_file, image_id.value)

        cls.is_valid(
            identifier,
            path,
            attrs,
        )

        return Image(
            identifier,
            path,
            attrs,
        )
