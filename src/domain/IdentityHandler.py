from ..infraestructure.InfraestructureError import InfraestructureError
from ..presentation.IdentifierHandler import IdentifierHandler
from ..utils.ErrorHandler import ID_NOT_FOUND
from .DomainError import DomainError
from .RepositoryProtocol import RepositoryProtocol


class IdentityHandler:
    value = None

    def __init__(
        self, ref_repository: RepositoryProtocol, identifier: IdentifierHandler
    ) -> None | DomainError:
        try:
            ref_repository.entityExists(identifier)
            self.value = identifier
        except InfraestructureError:
            raise DomainError(ID_NOT_FOUND, "Ticket doesnt exists")
