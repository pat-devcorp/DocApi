import pytest

from src.domain.DomainError import DomainError
from src.domain.model.person import Person, PersonDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.person import PersonController
from src.utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH


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
    u = UserService.get_mock()
    r = MockRepositoryClient()
    b = MockBrokerClient()
    return TicketController(u, r, b)


def get_obj():
    obj_id = PersonDomain.get_identifier()
    print(f"ID:{obj_id}")
    obj = PersonDomain.new(obj_id, "ready")
    print(f"OBJECT:{obj}")
    return obj


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
