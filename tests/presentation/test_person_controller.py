import pytest

from src.domain.DomainError import DomainError
from src.domain.model.person import PersonDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController
from src.utils.response_code import ID_NOT_VALID, INVALID_FORMAT


class MockRepositoryClient:
    object = {
        "personId": "194336c0-7c27-414c-a936-a14962618bec",
        "name": "Patrick Alonso",
        "lastName": "Fuentes Carpio",
        "mailAddress": "patrick18483@gmail.com",
        "birthDate": None,
        "documentNumber": None,
        "address": None,
    }

    def dsn(self):
        return "mock-repos"

    def fetch(self, attrs, matching):
        return [self.object]

    def get_by_id(self, identifier, attrs):
        return self.object

    def delete(self, identifier) -> None:
        return None

    def update(self, identifier, kwargs) -> None:
        return None

    def delete(self, kwargs) -> None:
        return None


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient()
    b = MockBrokerClient()
    return PersonController(u, r, b)


def test_domain():
    person_id = PersonDomain.get_default_identifier()
    print(f"ID:{PersonDomain.as_dict(person_id)}")
    person_1 = PersonDomain.new(
        person_id, "Patrick Alonso", "Fuentes Carpio", "patrick18483@gmail.com"
    )
    data_1 = PersonDomain.as_dict(person_1)
    print(f"OBJECT:{data_1}")
    attrs = {
        "birthDate": "1995/07/18",
        "documentNumber": "72539751",
        "address": "Cultura chimu 413",
    }
    person_2 = PersonDomain.new(
        person_id, "Patrick Alonso", "Fuentes Carpio", "patrick18483@gmail.com", **attrs
    )
    print(f"OBJECT:{PersonDomain.as_dict(person_2)}")
    person = {
        "personId": person_id.value,
        "name": "Patrick Alonso",
        "lastname": "Fuentes Carpio",
        "mailAddress": "patrick18483@gmail.com",
        "address": "Cultura chimu 413",
    }
    person_3 = PersonDomain.from_dict(person)
    print(f"OBJECT:{PersonDomain.as_dict(person_3)}")


def test_interface_invalid_params():
    tc = get_mock_controller()
    person_id = PersonDomain.get_default_identifier()
    valid_obj = {
        "personId": person_id.value,
        "name": "Patrick Alonso",
        "lastname": "Fuentes Carpio",
        "mailAddress": "patrick18483@gmail.com",
        "address": "Cultura chimu 413",
    }
    invalid_obj = {
        "personId": "0000",
        "name": "Patrick Al0ns0",
        "lastName": "Fuentes Carpi0",
        "mailAddress": "patrick",
    }

    with pytest.raises(DomainError) as error:
        tc.create(**invalid_obj)
        assert error.code == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.get_by_id(invalid_obj["personId"])
        assert str(error.code) == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.delete(invalid_obj["personId"])
        assert str(error.code) == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.create(
            valid_obj["personId"],
            invalid_obj["name"],
            invalid_obj["lastName"],
            invalid_obj["mailAddress"],
        )
        assert str(error.value) == INVALID_FORMAT[0]
