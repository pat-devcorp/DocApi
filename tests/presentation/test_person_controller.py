import pandas as pd
import pytest

from src.domain.DomainError import DomainError
from src.domain.identifier_handler import IdentifierHandler
from src.domain.model.person import Person, PersonDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController
from src.utils.status_code import ID_NOT_VALID, INVALID_FORMAT


class MockRepositoryClient:
    obj = {
        "person_id": IdentifierHandler.get_uuid_v4(),
        "name": "Patrick Alonso",
        "last_name": "Fuentes Carpio",
        "mail_address": "patrick18483@gmail.com",
        "birthdate": None,
        "document_number": None,
        "address": None,
    }

    def dsn(self):
        return "mock-repos"

    def fetch(self, attrs, matching):
        return [self.obj]

    def get_by_id(self, identifier, attrs):
        return self.obj

    def delete(self, identifier) -> None:
        return None

    def update(self, identifier, kwargs) -> None:
        return None

    def create(self, kwargs) -> None:
        return None

    def insert_many(self, data) -> None:
        return None


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient()
    b = MockBrokerClient()
    return PersonController(u, r, b)


def test_domain():
    identifier = PersonDomain.get_default_identifier()
    assert hasattr(identifier, "value")
    valid_obj = {
        "name": "Patrick Alonso",
        "last_name": "Fuentes Carpio",
        "mail_address": "patrick18483@gmail.com",
    }
    defaults = {
        "birthdate": "1995/07/18",
        "document_number": "72539751",
    }
    attrs = {
        "address": "Cultura chimu 413",
        "zip_code": "04002",
    }
    obj_1 = PersonDomain.new(identifier, **valid_obj)
    assert isinstance(obj_1, Person)
    assert isinstance(PersonDomain.as_dict(obj_1), dict)
    obj_2 = PersonDomain.new(identifier, **valid_obj, **defaults, attrs=attrs)
    assert isinstance(obj_2, Person)
    dct = dict(valid_obj)
    dct.update({"person_id": identifier.value})
    obj_3 = PersonDomain.from_dict(dct)
    assert isinstance(obj_3, Person)


def test_interface_invalid_params():
    tc = get_mock_controller()
    person_id = PersonDomain.get_default_identifier()
    valid_obj = {
        "person_id": person_id.value,
        "name": "Patrick Alonso",
        "lastname": "Fuentes Carpio",
        "mail_address": "patrick18483@gmail.com",
        "address": "Cultura chimu 413",
    }
    invalid_obj = {
        "person_id": "0000",
        "name": "Patrick Al0ns0",
        "last_name": "Fuentes Carpi0",
        "mail_address": "patrick",
    }

    with pytest.raises(DomainError) as error:
        tc.create(**invalid_obj)
        assert error.code == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.get_by_id(invalid_obj["person_id"])
        assert str(error.code) == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.delete(invalid_obj["person_id"])
        assert str(error.code) == ID_NOT_VALID[0]

    with pytest.raises(DomainError) as error:
        tc.create(
            person_id.value,
            invalid_obj["name"],
            invalid_obj["last_name"],
            invalid_obj["mail_address"],
        )
        assert str(error.value) == INVALID_FORMAT[0]
