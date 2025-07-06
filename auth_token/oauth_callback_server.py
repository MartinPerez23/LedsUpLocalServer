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
            self.send_header('Location', 'https://ledsupwebserver.onrender.com/ledsup/autenticado/')
            self.end_headers()
        elif self.path == "/favicon.ico":
            self.send_response(204)  # No Content
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

def run_server():
    with socketserver.TCPServer(("127.0.0.1", PORT), OAuthCallbackHandler) as httpd:
        print(f"Escuchando en http://localhost:{PORT}/callback ...")
        while OAuthCallbackHandler.code is None:
            httpd.handle_request()
        return OAuthCallbackHandler.code