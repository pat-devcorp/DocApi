from enum import Enum

from ...domain.identifier_handler import Identifier
from ...domain.model.person import Person
from ...utils.response_code import DB_ID_NOT_FOUND
from ..ApplicationError import ApplicationError
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..criteria import Criteria
from ..RepositoryProtocol import RepositoryProtocol


class ImageEvent(Enum):
    JPG = 0
    PNG = 1


# TODO: Rule to manager can not have in progress more than 4 Images
class PersonUseCase:
    def __init__(
        self,
        ref_write_uid: Identifier,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Image._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields
