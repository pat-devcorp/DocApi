from ..infraestructure.InfraestructureError import InfraestructureError
from ..presentation.IdentifierHandler import IdentifierHandler
from ..utils.ErrorHandler import ID_NOT_FOUND
from .DomainError import DomainError
from .RepositoryProtocol import RepositoryProtocol


class IdentityHandler:
    value = None

    def __init__(self, identifier: IdentifierHandler) -> None | DomainError:
        self.value = identifier

    @classmethod
    def ensureIdentity(
        cls, ref_repository: RepositoryProtocol, identifier: IdentifierHandler
    ) -> None | DomainError:
        try:
            ref_repository.entityExists(identifier)
            return cls(identifier)
        except InfraestructureError:
            raise DomainError(ID_NOT_FOUND, "Ticket doesnt exists")
