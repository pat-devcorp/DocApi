import logging
import os
import sys
from concurrent import futures
from dotenv import find_dotenv, load_dotenv

import grpc
from grpc_reflection.v1alpha import reflection

from .build import hello_world_pb2, hello_world_pb2_grpc, task_pb2, task_pb2_grpc

logger = logging.getLogger(__name__)

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, ".."))
# from .task_pb2 import CreateTaskResponse
# from .task_pb2_grpc import add_TaskServicer_to_server
from src.infrastructure.bootstrap.app import App
from src.presentation.controller.task import TaskController


class Greeter(hello_world_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        return hello_world_pb2.HelloReply(message=f"Hello, {request.name}!")

    def SayHelloAgain(self, request, context):
        return hello_world_pb2.HelloReply(message=f"Hello again, {request.name}!")


class Task(task_pb2_grpc.TaskServicer):
    def CreateTask(self, request, context):
        # Extract parameters from the request
        writeUId = request.writeUId
        taskId = request.taskId
        channelType = request.channelType
        requirement = request.requirement
        because = request.because

        myConfig = App()
        # Create a TaskController instance
        lc = TaskController(
            writeUId,
            myConfig.Mongo,
            myConfig.Rabbitmq,
        )

        # Call the create method on the TaskController
        _ = lc.create(
            taskId,
            channelType,
            requirement,
            because,
        )

        # Return a response indicating success
        return task_pb2.CreateTaskResponse(ok="OK")


def create_server():
    load_dotenv(find_dotenv())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    hello_world_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    task_pb2_grpc.add_TaskServicer_to_server(Task(), server)

    SERVICE_NAMES = (
        hello_world_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name,
        task_pb2.DESCRIPTOR.services_by_name["Task"].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    create_server()
