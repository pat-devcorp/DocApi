from collections import namedtuple

Person = namedtuple(
    "Person",
    ["personId", "name", "lastName", "contactIds"],
)
PartialPerson = namedtuple(
    "PartialPerson",
    Person._fields + ["birthDate", "documentNumber", "address"],
)
