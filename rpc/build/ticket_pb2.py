# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: task.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'task.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ctask.proto\"\xb4\x01\n\x13\x43reateTaskRequest\x12\x10\n\x08writeUId\x18\x01 \x01(\t\x12\x10\n\x08taskId\x18\x02 \x01(\t\x12\'\n\x0b\x63hannelType\x18\x03 \x01(\x0e\x32\x12.TaskChannelType\x12\x13\n\x0brequirement\x18\x04 \x01(\t\x12\x0f\n\x07\x62\x65\x63\x61use\x18\x05 \x01(\t\x12 \n\x05state\x18\x06 \x01(\x0e\x32\x0c.TaskStateH\x00\x88\x01\x01\x42\x08\n\x06_state\"\"\n\x14\x43reateTaskResponse\x12\n\n\x02ok\x18\x01 \x01(\t*\x1d\n\x11TaskChannelType\x12\x08\n\x04MAIL\x10\x00*M\n\x0bTaskState\x12\x0b\n\x07\x43REATED\x10\x00\x12\x0b\n\x07\x44\x45LETED\x10\x01\x12\x0e\n\nIN_PROCESS\x10\x02\x12\x0b\n\x07OBSERVE\x10\x03\x12\x07\n\x03\x45ND\x10\x04\x32\x45\n\x06Task\x12;\n\x0c\x43reateTask\x12\x14.CreateTaskRequest\x1a\x15.CreateTaskResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'task_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TICKETCHANNELTYPE']._serialized_start=235
  _globals['_TICKETCHANNELTYPE']._serialized_end=264
  _globals['_TICKETSTATE']._serialized_start=266
  _globals['_TICKETSTATE']._serialized_end=343
  _globals['_CREATETICKETREQUEST']._serialized_start=17
  _globals['_CREATETICKETREQUEST']._serialized_end=197
  _globals['_CREATETICKETRESPONSE']._serialized_start=199
  _globals['_CREATETICKETRESPONSE']._serialized_end=233
  _globals['_TICKET']._serialized_start=345
  _globals['_TICKET']._serialized_end=414
# @@protoc_insertion_point(module_scope)
