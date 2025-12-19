import json

LIBROS = [
    {"id": 1, "titulo": "La Odisea", "autor": "Homero", "anio": 1400}
]
NEXT_ID = 2 

# Funciones
def json_response(start_response, data, status="200 OK"):
    # Envia una respuesta
    headers = [("Content-Type", "application/json; charset=utf-8")]
    start_response(status, headers)
    return [json.dumps(data, ensure_ascii=False).encode("utf-8")]

def not_found(start_response, msg="No encontrado"):
    # Envia un error
    start_response("404 Not Found", [("Content-Type", "application/json")])
    return [json.dumps({"error": msg}).encode("utf-8")]

def parse_body(environ):
    try:
        length = int(environ.get("CONTENT_LENGTH", "0"))
    except ValueError:
        length = 0
    
    body = environ["wsgi.input"].read(length) if length > 0 else b""
    return body.decode("utf-8")

# Aplicacion principal
def app(environ, start_response):
    global NEXT_ID
    
    # Obtiene el metodo
    metodo = environ.get("REQUEST_METHOD", "GET")
    path = environ.get("PATH_INFO", "/")
    
    print(f"[{metodo}] {path}") 
    
    # Listar los libros
    if metodo == "GET" and path == "/libros":
        return json_response(start_response, {"libros": LIBROS, "total": len(LIBROS)})
    
    # Obtener los libros
    elif metodo == "GET" and path.startswith("/libros/"):
        try:
            libro_id = int(path.split("/")[-1]) 
        except ValueError:
            return not_found(start_response, "ID inválido")
        
        # Buscar libro
        for libro in LIBROS:
            if libro["id"] == libro_id:
                return json_response(start_response, libro)
        
        return not_found(start_response, f"Libro con ID {libro_id} no encontrado")
    
    # Crear libro
    elif metodo == "POST" and path == "/libros":
        raw_body = parse_body(environ)
        
        try:
            datos = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError:
            return json_response(start_response, 
                               {"error": "JSON inválido"}, 
                               status="400 Bad Request")
        # Valida
        titulo = datos.get("titulo", "").strip()
        autor = datos.get("autor", "").strip()
        anio = datos.get("anio")
        
        if not titulo or not autor or anio is None:
            return json_response(start_response, {"error": "Campos requeridos: titulo, autor, anio"}, status="400 Bad Request")
        
        try:
            anio = int(anio)  # Convertir a entero
        except (ValueError, TypeError):
            return json_response(start_response,{"error": "El año debe ser un número"}, status="400 Bad Request")
        
        # Crear el libro
        nuevo_libro = {
            "id": NEXT_ID,
            "titulo": titulo,
            "autor": autor,
            "anio": anio
        }
        
        LIBROS.append(nuevo_libro)
        NEXT_ID += 1
        
        return json_response(start_response, nuevo_libro, status="201 Created")
    
    # Pagina inicial
    elif metodo == "GET" and path == "/":
        html = """
        <html>
            <body>
                <h1>Libros</h1>
            </body>
        </html>
        """
        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [html.encode("utf-8")]
    
    # Ruta no encontrada
    else:
        return not_found(start_response)