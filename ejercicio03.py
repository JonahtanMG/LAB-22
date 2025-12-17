from http.server import BaseHTTPRequestHandler, HTTPServer

class MiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
            <html>
                <body>
                    <h1>Servidor</h1>
                </body>
            </html>
            """)
        elif self.path == '/saludo':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"msg": "Hola"}')
        else:
            self.wfile.write(b"Ruta no encontrada")

server = HTTPServer(("localhost", 8000), MiHandler)
print("Servidor corriendo en http://localhost:8000")
server.serve_forever()