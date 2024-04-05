from ...application.use_case.person import PersonUseCase
from ...domain.enum.contact_type import ContactType
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
        _r = PersonMongo(ref_repository)
        _b = ref_broker
        self._uc = PersonUseCase(_w, _r, _b)

    def fetch(self) -> list:
        return self._uc.fetch(0)

    def get_by_id(self, person_id):
        person_id = PersonDomain.set_identifier(person_id)

        return self._uc.get_by_id(person_id)

    def delete(self, person_id):
        person_id = PersonDomain.set_identifier(person_id)

        return self._uc.delete(person_id)

    def update(self, person_id, params: dict):
        params.update({"person_id": person_id})
        obj = PersonDomain.from_dict(params)

        return self._uc.update(obj)

    def create(
        self,
        person_id,
        name,
        last_name,
        contact_type,
        birthdate=None,
        document_number=None,
        address=None,
    ):
        person_id = PersonDomain.set_identifier(person_id)
        contact = ContactType(contact_type)
        obj = PersonDomain.new(
            person_id,
            name,
            last_name,
            contact,
            birthdate,
            document_number,
            address,
        )

        return self._uc.create(obj)

    def insert_many(self, data: list):
        return self._uc.insert_many(data)
