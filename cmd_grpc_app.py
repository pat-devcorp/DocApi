import os
import sys

from rpc.server import create_server

if __name__ == "__main__":
    app = create_server()
    app.start()
    app.wait_for_termination()
