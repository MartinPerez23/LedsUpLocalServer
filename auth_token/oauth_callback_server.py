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
            self.send_response(302)
            self.send_header('Location', 'https://127.0.0.1:8000/ledsup/autenticado/')
            self.end_headers()
            self.wfile.write(b"<html><body>Redirigiendo...</body></html>")
        else:
            self.send_response(404)
            self.end_headers()


def run_server():
    with socketserver.TCPServer(("127.0.0.1", PORT), OAuthCallbackHandler) as httpd:
        print(f"Escuchando en https://localhost:{PORT}/callback ...")
        httpd.handle_request()
        return OAuthCallbackHandler.code
