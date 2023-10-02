from src.infraestructure.server import createServer

if __name__ == "__main__":
    app = createServer()
    app.run()
