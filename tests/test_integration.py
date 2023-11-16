from src.domain.dao.ticket import TicketDAO
from src.infraestructure.broker.brokermock import BrokerMock
from src.infraestructure.repositories.RepositoryMock import RepositoryMock
from src.infraestructure.repositories.ticket_mongo import Ticket as TicketRepository
from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.dto.ticket import TicketHandler


def getUser():
    return "9999"


def getData():
    dto = TicketHandler.getMock()
    dao = TicketDAO.getMock()
    return (
        dao["ticket_id"],
        dto,
    )


def getControllerMock(write_uid, obj_id, obj):
    my_repository = RepositoryMock(obj_id, obj)
    my_producer = BrokerMock()
    return TicketController(write_uid, my_repository, my_producer)


def test_task_fake():
    obj_id, obj = getData()
    lc = getControllerMock(obj_id, obj, getUser())
    assert lc.create(obj_id, obj)


def test_task():
    current_user = getUser()
    obj_id, obj = getData()
    r = TicketRepository()
    lc = TicketController(current_user)
    lc = getControllerMock(obj_id, obj, getUser())
    assert lc.create(obj_id, obj)
