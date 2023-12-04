from src.domain.dao.ticket import TicketDAO
from src.domain.DomainError import DomainError
from src.infraestructure.broker.brokermock import BrokerMock
from src.infraestructure.repositories.RepositoryMock import RepositoryMock
from src.infraestructure.repositories.ticket_mongo import Ticket as TicketRepository
from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.dto.ticket import TicketDTO


def getUser():
    return "9999"


def test_TaskController():
    dto = TicketDTO.getMock()
    my_repository = RepositoryMock(dto.asDict())
    my_producer = BrokerMock()
    lc = TicketController(getUser(), my_repository, my_producer)
    assert lc.create(dto)


def test_TaskUseCase():
    current_user = getUser()
    dto = TicketDTO.getMock()
    r = TicketRepository()
    lc = TicketController(current_user, r)
    try:
        lc.getByID(dto.ticket_id)
    except DomainError as eu:
        assert True
    lc.create(dto)
    data = lc.getByID(dto.ticket_id)
    print(f"DATA: {data}")
    assert data
    dto.description = "I was updated successfully"
    lc.update(dto)
    datos = lc.fetch()
    print(f"DATOS: {datos}")
    assert datos
    lc.delete(dto.ticket_id)
