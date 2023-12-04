from ..infraestructure.InfraestructureError import InfraestructureError
from ..presentation.IdentifierHandler import IdentifierHandler
from ..utils.ResponseHandler import ID_NOT_FOUND
from .DomainError import DomainError
from .RepositoryProtocol import RepositoryProtocol


class IdentityHandler:
    value = None

    def __init__(self, identifier) -> None | DomainError:
        self.value = identifier

    @classmethod
    def create(cls, identifier: IdentifierHandler) -> None | DomainError:
        return cls(identifier.value)

    @classmethod
    def ensureIdentity(
        cls, ref_repository: RepositoryProtocol, identifier: IdentifierHandler
    ) -> None | DomainError:
        try:
            ref_repository.entityExists(identifier.value)
            return cls(identifier.value)
        except InfraestructureError:
            raise DomainError(ID_NOT_FOUND, "Ticket doesnt exists")
