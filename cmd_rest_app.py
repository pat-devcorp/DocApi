import os
import sys

from rest.server import create_server

app = create_server()

if __name__ == "__main__":
    app.run()
