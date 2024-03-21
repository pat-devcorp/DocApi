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

    def get_by_id(self, obj_id):
        personId = PersonDomain.set_identifier(obj_id)

        return self._uc.get_by_id(personId)

    def delete(self, obj_id):
        personId = PersonDomain.set_identifier(obj_id)

        return self._uc.delete(personId)

    def update(self, obj_id, params: dict):
        personId = PersonDomain.set_identifier(obj_id)
        obj = PersonDomain.from_dict(personId, params)

        return self._uc.update(obj)

    def create(self, obj_id, name, lastName):
        personId = PersonDomain.set_identifier(obj_id)
        obj = PersonDomain.new(personId, name, lastName)

        return self._uc.create(obj)
