import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = 34123

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    code = None

    def do_GET(self):
        if self.path.startswith("/callback"):
            query = urlparse(self.path).query
            params = parse_qs(query)
            OAuthCallbackHandler.code = params.get('code', [None])[0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            msg = "<html><body><h1>Autenticacion completada</h1>Ya puedes cerrar esta ventana.</body></html>"
            self.wfile.write(msg.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    with socketserver.TCPServer(("localhost", PORT), OAuthCallbackHandler) as httpd:
        print(f"Escuchando en http://localhost:{PORT}/callback ...")
        httpd.handle_request()  # Solo espera una petición y después termina
        return OAuthCallbackHandler.code