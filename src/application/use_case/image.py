from enum import Enum

from ...domain.identifier_handler import IdentifierHandler
from ...domain.model.image import Image, ImageDomain
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..RepositoryProtocol import RepositoryProtocol


class ImageEvent(Enum):
    JPG = 0
    PNG = 1


class ImageUseCase:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Image._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def create(self, obj: Image) -> None:
        item = ImageDomain.as_dict(obj)
        item.update(AuditHandler.get_create_fields(self._w))

        self._r.create(item)

        ImageDomain.save(obj)
