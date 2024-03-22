from ...application.use_case.person import PersonUseCase
from ...domain.model.person import PersonDomain
from ...infrastructure.mongo.repositories.person_mongo import PersonMongo


class PersonController:
    def __init__(
        self,
        ref_write_uid,
        ref_repository,
        ref_broker,
    ) -> None:
        _w = ref_write_uid
        _r = PersonMongo(ref_repository, PersonDomain.pk)
        _b = ref_broker
        self._uc = PersonUseCase(_w, _r, _b)

    def fetch(self) -> list:
        return self._uc.fetch(0)

    def get_by_id(self, personId):
        personId = PersonDomain.set_identifier(personId)

        return self._uc.get_by_id(personId)

    def delete(self, personId):
        personId = PersonDomain.set_identifier(personId)

        return self._uc.delete(personId)

    def update(self, personId, params: dict):
        params.update({"personId": personId})
        obj = PersonDomain.from_dict(params)

        return self._uc.update(obj)

    def create(
        self,
        personId,
        name,
        lastName,
        mailAddress,
        birthDate=None,
        documentNumber=None,
        address=None,
    ):
        personId = PersonDomain.set_identifier(personId)
        obj = PersonDomain.new(
            personId, name, lastName, mailAddress, birthDate, documentNumber, address
        )

        return self._uc.create(obj)
