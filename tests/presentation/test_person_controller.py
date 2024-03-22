import pytest

from src.domain.model.person import PersonDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController


class MockRepositoryClient:
    object = []

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
    person_1 = PersonDomain.new(person_id, "Patrick Alonso", "Fuentes Carpio", "patrick18483@gmail.com")
    data_1 = PersonDomain.as_dict(person_1)
    print(f"OBJECT:{data_1}")
    attrs = {"birthDate": "1995/07/18", "documentNumber": "72539751", "address": "Cultura chimu 413"}
    person_2 = PersonDomain.new(person_id, "Patrick Alonso", "Fuentes Carpio", "patrick18483@gmail.com", attrs)
    obj_from_dict = PersonDomain.from_dict(data_1)
    print(f"OBJECT:{PersonDomain.as_dict(obj_from_dict)}")
    # return obj_id, new_obj


# def get_invalid_obj():
#     return Ticket(
#         "a",
#         "a" * 201,
#         100,
#         100,
#         100,
#         100,
#         "20/20/20",
#     )


# def test_interface_with_out_parameters():
#     tc = get_mock_controller()

#     with pytest.raises(TypeError) as error:
#         tc.create()
#     with pytest.raises(TypeError) as error:
#         tc.update()
#     with pytest.raises(TypeError) as error:
#         tc.delete()


# def test_interface_invalid_params():
#     tc = get_mock_controller()
#     obj = get_obj()
#     invalid_obj = get_invalid_obj()

#     with pytest.raises(DomainError) as error:
#         tc.create(invalid_obj.ticketId, invalid_obj.requirement)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.get_by_id(invalid_obj.ticketId)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.delete(invalid_obj.ticketId)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.create(obj.ticketId, invalid_obj.requirement)
#     assert str(error.value) == SCHEMA_NOT_MATCH[1]

#     with pytest.raises(DomainError) as error:
#         tc.update(obj.ticketId, invalid_obj._asdict())
#     assert str(error.value) == SCHEMA_NOT_MATCH[1]
