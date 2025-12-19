from wsgiref.simple_server import make_server
from libros import app

if __name__ == "__main__":
    server = make_server("", 8000, app)
    print("Servidor WSGI Libros en http://localhost:8000")
    server.serve_forever()