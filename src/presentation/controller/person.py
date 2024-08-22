from utils.timeout import timeout_function
from ...application.use_case.person import PersonUseCase
from ...domain.enum.contact_type import ContactType
from ...domain.model.person import PersonDomain
from ...infrastructure.mongo.repositories.person_mongo import PersonMongo

# Time out per use case
class PersonController:
    def __init__(
        self,
        ref_write_uid,
        ref_env,
        ref_timeout,
    ) -> None:
        _w = ref_write_uid
        _r = PersonMongo(ref_env["REPOSITORY_MONGO"])
        _b = ref_env["BROKER_RABBITMQ"]
        self._t = ref_timeout
        self._uc = PersonUseCase(_w, _r, _b)

    def fetch(self) -> list:
        return timeout_function(
                self._uc.fetch(0), seconds=self._t
            )

    def get_by_id(self, person_id: str):
        person_id = PersonDomain.set_identifier(person_id)

        return timeout_function(
            self._uc.get_by_id(person_id), seconds=self._t
        )


    def delete(self, person_id: str):
        person_id = PersonDomain.set_identifier(person_id)

        return self._uc.delete(person_id)

    def update(self, person_id: str, params: dict):
        params.update({"person_id": person_id})
        obj = PersonDomain.from_dict(params)

        return self._uc.update(obj)

    def create(
        self,
        person_id: str,
        name: str,
        last_name: str,
        contact_type: int | ContactType,
        birthdate: str = None,
        document_number: str = None,
        address: str = None,
    ):
        person_id = PersonDomain.set_identifier(person_id)
        enum_contact = contact_type
        if isinstance(contact_type, int):
            enum_contact = ContactType(contact_type)
        obj = PersonDomain.new(
            person_id,
            name,
            last_name,
            enum_contact,
            birthdate,
            document_number,
            address,
        )

        return self._uc.create(obj)

    def insert_many(self, data: list):
        return self._uc.insert_many(data)
