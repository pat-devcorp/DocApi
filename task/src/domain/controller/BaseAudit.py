from ...domain.DomainProtocol import DomainProtocol
from ...domain.RepositoryProtocol import RepositoryProtocol
from ...domain.DomainError import DomainError
from ...utils.AuditHandler import AuditHandler
from ...utils.ErrorHandler import ID_NOT_FOUND
from ...utils.IdentityHandler import IdentityHandler


class BaseAuditRepository:
    def __init__(
            self,
            name:str,
            pk:str,
            write_uid:IdentityHandler,
            ref_domain:DomainProtocol,
            fields:list,
            repository:RepositoryProtocol,
        ):
        self.name = name
        self.pk = pk
        self.write_uid = write_uid
        self.domain = ref_domain
        self.fields = fields
        self.repository = repository

    def setFields(self, fields: list):
        self.fields = fields

    @classmethod
    def entityExists(
        cls, ref_repository, name, pk, identifier: IdentityHandler
    ) -> bool:
        return (
            True
            if ref_repository.getByID(name, pk, identifier, [pk]) is not None
            else False
        )

    def fetch(self) -> list:
        return self.repository.fetch(self.name, self.fields)

    def getByID(self, identifier: IdentityHandler) -> list:
        return self.repository.getByID(self.name, self.pk, identifier, self.fields)

    def delete(self, identifier: IdentityHandler) -> bool:
        if not self.entityExists(self.repository, self.name, self.pk, identifier):
            raise DomainError(ID_NOT_FOUND)

        self.repository.delete(self.name, self.pk, identifier)
        return True

    def create(self, params: dict) -> bool:
        data = self.ref_domain.create(params)
        my_audit = AuditHandler.create(self.write_uid)
        my_ticket = my_audit._asdict() | data

        self.repository.create(self.name, my_ticket)
        return True

    def update(self, params: dict) -> bool:
        if not self.entityExists(
            self.repository, self.name, self.pk, params.get(self.pk)
        ):
            raise DomainError(ID_NOT_FOUND)

        data = self.ref_domain.fromDict(params)
        my_audit = AuditHandler.getUpdateFields(self.write_uid)
        data.update(my_audit)

        self.repository.update(self.name, self.pk, data[self.pk], data)
        return True
