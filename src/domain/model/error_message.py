from collections import namedtuple


StatusMessage = namedtuple(
    "StatusMessage",
    [
        "id",
        "message",
    ],
)

LOGIC_CRASH = StatusMessage(message="Logic Crush")
FIELD_REQUIRED = StatusMessage(message="Field Required")
ID_NOT_FOUND = StatusMessage(message="ID must be provided")
ID_NOT_VALID = StatusMessage(message="ID not valid")
WRITER_NOT_FOUND = StatusMessage(message="Writer must be provided")
SCHEMA_NOT_MATCH = StatusMessage(message="Schema does not match")
INVALID_FORMAT = StatusMessage(message="Invalid format")
INVALID_OBJECT = StatusMessage(message="Invalid object")
UNSUPPORTED_MEDIA_TYPE = StatusMessage(message="This type of file is not supported")
WARNING_FILE = StatusMessage(message="File could have potential virus")
NOT_FOUND = StatusMessage(message="Not found")
OPERATION_FAIL = StatusMessage(message="Operation fail")
REQUIRED_FIELD = StatusMessage(message="Required param")
IS_NOT_MEMBER = StatusMessage(message="Is not member of")
BROKER_CONNECTION_FAIL = StatusMessage(message="Broker not responding")
BROKER_SEND_FAIL = StatusMessage(message="Broker attempt to send failed")
BROKER_CHANNEL_ERROR = StatusMessage(message="Broker channel have and error")
DUPLICATE_ID = StatusMessage(message="Id is present in repository")
DB_CONNECTION_FAIL = StatusMessage(message="Database not responding")
DB_COLLECTION_ERROR = StatusMessage(message="Table is not present in database")
DB_GET_FAIL = StatusMessage(message="Database attempt get")
DB_ID_NOT_FOUND = StatusMessage(message="Database attempt get by identifier")
DB_CREATE_FAIL = StatusMessage(message="Database attempt create")
DB_UPDATE_FAIL = StatusMessage(message="Database attempt update")
DB_DELETE_FAIL = StatusMessage(message="Database attempt delete")
HEADER_NOT_VALID = StatusMessage(message="Headers not valid")
