from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SumaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        mostrar = b'''
            <html>
                <body>
                    <h1>Servidor</h1>
                </body>
            </html>
            '''
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(mostrar)

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        datos = json.loads(body.decode("utf-8"))
        a = float(datos.get("a"))
        b = float(datos.get("b"))
        suma = a+b
        respuesta = {
            "resultado" : suma
        }

        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), SumaHandler)
    print("Servidor de suma corriendo en http://localhost:8000")
    print("Envía POST con JSON: {\"a\": 5, \"b\": 3}")
    server.serve_forever()


        