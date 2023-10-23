from src.infraestructure.repositories.repositorymock import RepositoryMock
from src.infraestructure.broker.brokermock import BrokerMock
from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.interface.InterfaceError import InterfaceError
from src.presentation.interface.ticket import Ticket as TicketInterface
from src.presentation.interface.ticket import TicketDTO


def test_interface_user_required():
    try:
        test_ticket_dto = {
            "write_uid": "9999",
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def test_interface_id_required():
    try:
        test_ticket_dto = {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def assert_type_dto():
    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_dto = TicketInterface.fromDict(test_ticket_dto)
    assert isinstance(my_ticket_dto, TicketDTO)


## Basic task methods
def getControllerMock():
    my_repository = RepositoryMock()
    my_producer = BrokerMock()
    return TicketController(my_repository, my_producer)

def test_controller_create():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "description": "This is a ticket",
    }
    my_ticket_create_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.create(my_ticket_create_dto)
    assert response


def test_controller_get():
    my_ticket_controller = getControllerMock()

    response_get = my_ticket_controller.fetch()
    assert isinstance(response_get, list)


def test_controller_update():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "8888",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "description": "This is a ticket modified",
    }
    my_ticket_update_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.update(my_ticket_update_dto)
    assert response


def test_controller_get_by_id():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_get_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.getByID(my_ticket_get_dto)
    assert isinstance(response, dict)


def test_controller_delete():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_delete_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.delete(my_ticket_delete_dto)
    assert response


def test_task_member():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "member_id": "8888",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addMember(my_ticket_member_dto)
    assert response


## Aggregate for task
def test_task_keyword():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "keyword": "test",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addKeyword(my_ticket_member_dto)
    assert response


def test_task_meeting():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "subject": "Dealing with bugs",
        "meeting_date": "03/10/2023 16:30",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addKeyword(my_ticket_member_dto)
    assert response


def test_task_cheklist():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "checklist": "Milestone for Project",
        "items": [
            "get notifications about project",
            "generate documentation for project"
        ],
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addKeyword(my_ticket_member_dto)
    assert response


def test_task_attachment():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "attachment_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addKeyword(my_ticket_member_dto)
    assert response


def test_task_assignee():
    my_ticket_controller = getControllerMock()

    test_ticket_dto = {
        "write_uid": "9999",
        "estimate_time_in_minutes": "240",
        "end_at": "03/10/2023 16:30",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_member_dto = TicketInterface.fromDict(test_ticket_dto)
    response = my_ticket_controller.addKeyword(my_ticket_member_dto)
    assert response