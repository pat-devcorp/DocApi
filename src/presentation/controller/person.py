from ...application.use_case.Person import PersonUseCase
from ...domain.model.Person import PersonDomain
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
        PersonId = PersonDomain.set_identifier(obj_id)

        return self._uc.get_by_id(PersonId)

    def delete(self, obj_id):
        PersonId = PersonDomain.set_identifier(obj_id)

        return self._uc.delete(PersonId)

    def update(self, obj_id, params: dict):
        PersonId = PersonDomain.set_identifier(obj_id)
        obj = PersonDomain.from_dict(PersonId, params)

        return self._uc.update(obj)

    def create(self, obj_id, channelId, requirement, because):
        PersonId = PersonDomain.set_identifier(obj_id)
        obj = PersonDomain.new(PersonId, channelId, requirement, because)

        return self._uc.create(obj)
