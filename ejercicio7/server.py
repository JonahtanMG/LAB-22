from wsgiref.simple_server import make_server
from urllib.parse import unquote
import json, os, mimetypes

# Carpeta con los archivos
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Datos inicializados
EQUIPOS = [
    {"id": 1, "nombre": "Real Madrid", "ciudad": "Madrid", "nivelAtaque": 10, "nivelDefensa": 9},
    {"id": 2, "nombre": "Barcelona", "ciudad": "Barcelona", "nivelAtaque": 9, "nivelDefensa": 8},
]
# Contador para asignar IDs nuevos 
NEXT_ID = 3

def read_body(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH", "0"))
    except ValueError:
        length = 0
    return environ["wsgi.input"].read(length) if length > 0 else b""

def serve_static(path, start_response):
    # Evita que el path empiece con "/" para construir rutas de archivos
    safe_path = path.lstrip("/")
    full_path = os.path.join(STATIC_DIR, safe_path.replace("static/", ""))
    if not os.path.isfile(full_path):
        start_response("404 Not Found", [("Content-Type", "text/plain")])
        return [b"Archivo no encontrado"]

    ctype, _ = mimetypes.guess_type(full_path)
    if ctype is None:
        ctype = "application/octet-stream"

    with open(full_path, "rb") as f:
        content = f.read()

    start_response("200 OK", [("Content-Type", ctype)])
    return [content]

def json_response(start_response, data, status="200 OK"):
    # Respuesta estándar JSON
    start_response(status, [("Content-Type", "application/json")])
    return [json.dumps(data).encode("utf-8")]

def not_found(start_response, msg="Ruta no encontrada"):
    # 404 en JSON
    start_response("404 Not Found", [("Content-Type", "application/json")])
    return [json.dumps({"error": msg}).encode("utf-8")]

def app(environ, start_response):
    global NEXT_ID 

    # Método HTTP y ruta solicitada
    metodo = environ.get("REQUEST_METHOD", "GET")
    path = unquote(environ.get("PATH_INFO", "/")) 

    # Ruta
    if metodo == "GET" and path == "/":
        return serve_static("/static/index.html", start_response)

    if path.startswith("/static/"):
        return serve_static(path, start_response)

    # Devuelve todos los equipos
    if metodo == "GET" and path == "/equipos":
        return json_response(start_response, EQUIPOS)

    # Devuelve un equipo por id
    if metodo == "GET" and path.startswith("/equipos/"):
        parts = path.strip("/").split("/") 
        if len(parts) == 2 and parts[0] == "equipos":
            try:
                eid = int(parts[1]) 
            except ValueError:
                return not_found(start_response, "ID invalido")

            # Busca en la lista 
            for equipo in EQUIPOS:
                if equipo["id"] == eid:
                    return json_response(start_response, equipo)

            return not_found(start_response, "Equipo no encontrado")

    # Crea un equipo nuevo
    if metodo == "POST" and path == "/equipos":
        raw = read_body(environ) 
        try:
            data = json.loads(raw.decode("utf-8")) if raw else {}
        except json.JSONDecodeError:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": "JSON invalido"}).encode("utf-8")]

        # Extrae campos del JSON
        nombre = data.get("nombre")
        ciudad = data.get("ciudad")
        nivelAtaque = data.get("nivelAtaque")
        nivelDefensa = data.get("nivelDefensa")

        # Validación básica
        if not nombre or not ciudad or nivelAtaque is None or nivelDefensa is None:
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": "Campos requeridos: nombre, ciudad, nivelAtaque, nivelDefensa"}).encode("utf-8")]

        try:
            na = int(nivelAtaque)
            nd = int(nivelDefensa)
        except (TypeError, ValueError):
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": "nivelAtaque y nivelDefensa deben ser numeros"}).encode("utf-8")]

        # Rango permitido
        if not (1 <= na <= 10 and 1 <= nd <= 10):
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": "niveles deben estar entre 1 y 10"}).encode("utf-8")]

        # Crea el nuevo equipo con ID 
        equipo = {"id": NEXT_ID, "nombre": nombre, "ciudad": ciudad, "nivelAtaque": na, "nivelDefensa": nd}
        EQUIPOS.append(equipo)
        NEXT_ID += 1  
        return json_response(start_response, equipo, status="201 Created")

    # Cualquier otra ruta
    return not_found(start_response)

if __name__ == "__main__":
    server = make_server("", 8000, app)
    print("Servidor WSGI en http://localhost:8000")
    server.serve_forever()