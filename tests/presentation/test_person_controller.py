import pandas as pd
import pytest

from src.domain.DomainError import DomainError
from src.domain.model.person import Person, PersonDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController
from src.utils.status_code import ID_NOT_VALID, INVALID_FORMAT

person_id = PersonDomain.get_default_identifier()
person = {
    "name": "Patrick Alonso",
    "last_name": "Fuentes Carpio",
    "mail_address": "patrick18483@gmail.com",
    "birthdate": "1995/07/18",
}
person_attrs = {
    "document_number": "72539751",
    "address": "Cultura chimu 413",
    "zip_code": "04002",
}
invalid_person_id = 0
invalid_person = {
    "name": "Patrick Al0ns0",
    "last_name": "Fuentes Carpi0",
    "mail_address": "patrick",
}


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient(person)
    b = MockBrokerClient()
    return PersonController(u, r, b)


def test_new_person():
    assert hasattr(person_id, "value")
    obj = PersonDomain.new(person_id, **person)
    assert isinstance(obj, Person)
    assert isinstance(PersonDomain.as_dict(obj), dict)


def test_new_person_with_attrs():
    obj = PersonDomain.new(person_id, **person, attrs=person_attrs)
    assert isinstance(obj, Person)
    assert isinstance(PersonDomain.as_dict(obj), dict)


def test_update_person():
    dct = dict(person)
    dct.update({"person_id": person_id.value})
    obj_3 = PersonDomain.from_dict(dct)
    assert isinstance(obj_3, Person)


def test_interface_invalid_params():
    tc = get_mock_controller()

    with pytest.raises(DomainError) as error:
        tc.create(invalid_person_id, **invalid_person)
        assert error.code == ID_NOT_VALID[0]

    # with pytest.raises(DomainError) as error:
    #     tc.get_by_id(invalid_obj["person_id"])
    #     assert str(error.code) == ID_NOT_VALID[0]

    # with pytest.raises(DomainError) as error:
    #     tc.delete(invalid_obj["person_id"])
    #     assert str(error.code) == ID_NOT_VALID[0]

    # with pytest.raises(DomainError) as error:
    #     tc.create(
    #         person_id.value,
    #         invalid_obj["name"],
    #         invalid_obj["last_name"],
    #         invalid_obj["mail_address"],
    #     )
    #     assert str(error.value) == INVALID_FORMAT[0]
