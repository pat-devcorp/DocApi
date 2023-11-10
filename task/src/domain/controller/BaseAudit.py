from ...domain.DomainError import DomainError
from ...utils.AuditHandler import AuditHandler

from ...utils.IdentityHandler import IdentityHandler


class BaseAuditRepository:
    _name = None
    _id = None
    _write_uid = None
    _repository = None
    _fields = None
    _func_filter = None

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in self._fields]

    @classmethod
    def entityExists(cls, ref_repository, identifier: IdentityHandler) -> bool:
        return (
            True
            if ref_repository.getByID(cls._name, cls._id, identifier, cls._name) is None
            else False
        )

    def fetch(self) -> list:
        return self._repository.get(self._name, self._fields)

    def getByID(self, identifier: IdentityHandler) -> list:
        return self._repository.getByID(self._name, self._id, identifier, self._fields)

    def delete(self, identifier: IdentityHandler) -> bool:
        if not self.entityExists(identifier):
            raise DomainError(["params does not exist"])

        self._repository.delete(self._name, self._id, identifier)
        return True

    def create(self, params: dict) -> bool:
        data = self._func_filter(params)
        my_audit = AuditHandler.create(self._write_uid)
        my_ticket = my_audit._asdict() | data

        self._repository.create(self._name, my_ticket)
        return True

    def update(self, params: dict) -> bool:
        print("---UPDATE---")
        if not self.entityExists(params.get(self._id)):
            raise DomainError(["params does not exist"])

        data = self._func_filter(params, False)
        my_audit = AuditHandler.getUpdateFields(self._write_uid)
        data.update(my_audit)

        self._repository.update(self._name, self._id, data[self._id], data)
        return True
