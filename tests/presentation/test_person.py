import unittest

import pandas as pd
import pytest

from src.domain.DomainError import DomainError
from src.domain.model.person import Person, PersonDomain
from src.domain.model.status_code import FIELD_REQUIRED, INVALID_FORMAT
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.my_mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController


class TestPersonController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.person = PersonDomain.get_valid_person()
        cls.person_id = PersonDomain.set_identifier(cls.person.person_id)
        cls.invalid_person = PersonDomain.get_invalid_person()
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(PersonDomain.as_dict(cls.person))
        b = MockBrokerClient()
        cls.controller = PersonController(u, r, b)

    def test_attrs(self):
        assert hasattr(self.person_id, "value")
        assert isinstance(PersonDomain.as_dict(self.person), dict)

    def test_new_person(self):
        obj = PersonDomain.new(
            self.person_id,
            self.person.name,
            self.person.last_name,
            self.person.contact_type,
        )
        assert isinstance(obj, Person)

    def test_new_person_with_attrs(self):
        obj = PersonDomain.new(
            self.person_id,
            self.person.name,
            self.person.last_name,
            self.person.contact_type,
            self.person.birthdate,
            self.person.document_number,
            self.person.attrs,
        )
        assert isinstance(obj, Person)

    def test_update_person(self):
        obj = PersonDomain.from_dict(PersonDomain.as_dict(self.person))
        assert isinstance(obj, Person)

    def test_interface_invalid_params(self):
        with pytest.raises(DomainError) as error:
            self.controller.create(
                None,
                self.invalid_person.name,
                self.invalid_person.last_name,
                self.invalid_person.contact_type,
            )
            assert error.code == FIELD_REQUIRED[0]

        with pytest.raises(DomainError) as error:
            self.controller.create(
                self.invalid_person.person_id,
                self.invalid_person.name,
                self.invalid_person.last_name,
                self.invalid_person.contact_type,
            )
            assert error.code == INVALID_FORMAT[0]


if __name__ == "__main__":
    unittest.main()
