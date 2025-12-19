from wsgiref.simple_server import make_server

def app(environ, start_response):
    path = environ.get("PATH_INFO","/")
    
    if path == "/":
        response = "<h1>Inicio</h1>"
    
    elif path == "/saludo":
        response = "<h1>Hola mundo desde WSGI</h1>"
    
    else:
        start_response("404 NOT FOUND",[("Content-Type", "text/html; charset=utf-8")])
        return [b"<h1>Pagina no encontrada</h1>"]
    
    start_response("200 OK", [("Content-Type", "text/html")])
    return [response.encode("utf-8")]

if __name__ == "__main__":
    with make_server("",8000,app) as server:
        print("Servidor corriendo en http://localhost:8000")
        server.serve_forever()