from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskChannelType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MAIL: _ClassVar[TaskChannelType]

class TaskState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CREATED: _ClassVar[TaskState]
    DELETED: _ClassVar[TaskState]
    IN_PROCESS: _ClassVar[TaskState]
    OBSERVE: _ClassVar[TaskState]
    END: _ClassVar[TaskState]
MAIL: TaskChannelType
CREATED: TaskState
DELETED: TaskState
IN_PROCESS: TaskState
OBSERVE: TaskState
END: TaskState

class CreateTaskRequest(_message.Message):
    __slots__ = ("writeUId", "taskId", "channelType", "requirement", "because", "state")
    WRITEUID_FIELD_NUMBER: _ClassVar[int]
    TICKETID_FIELD_NUMBER: _ClassVar[int]
    CHANNELTYPE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENT_FIELD_NUMBER: _ClassVar[int]
    BECAUSE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    writeUId: str
    taskId: str
    channelType: TaskChannelType
    requirement: str
    because: str
    state: TaskState
    def __init__(self, writeUId: _Optional[str] = ..., taskId: _Optional[str] = ..., channelType: _Optional[_Union[TaskChannelType, str]] = ..., requirement: _Optional[str] = ..., because: _Optional[str] = ..., state: _Optional[_Union[TaskState, str]] = ...) -> None: ...

class CreateTaskResponse(_message.Message):
    __slots__ = ("ok",)
    OK_FIELD_NUMBER: _ClassVar[int]
    ok: str
    def __init__(self, ok: _Optional[str] = ...) -> None: ...
