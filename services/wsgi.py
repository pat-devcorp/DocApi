from src.infraestructure.server import createServer

app = createServer()

if __name__ == "__main__":
    app.run()
