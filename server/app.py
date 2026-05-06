from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from garment_extractor import extract_garment


class GarmentHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._send_cors_headers(200)
        self.end_headers()

    def do_POST(self):
        if self.path != '/extract-garment':
            self._json_response(404, {'error': 'Not found'})
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length)
            data = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            self._json_response(400, {'error': 'Invalid JSON body'})
            return

        url = (data.get('url') or '').strip()
        if not url:
            self._json_response(400, {'error': 'Missing "url" field'})
            return

        try:
            result = extract_garment(url)
            self._json_response(200, result)
        except ValueError as e:
            self._json_response(400, {'error': str(e)})
        except (PermissionError, FileNotFoundError, TimeoutError, ConnectionError) as e:
            self._json_response(502, {'error': str(e)})
        except Exception as e:
            self._json_response(500, {'error': f'Extraction failed: {e}'})

    def _send_cors_headers(self, code):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def _json_response(self, code, data):
        body = json.dumps(data).encode('utf-8')
        self._send_cors_headers(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f'[{self.address_string()}] {fmt % args}', flush=True)


if __name__ == '__main__':
    port = 5050
    server = HTTPServer(('localhost', port), GarmentHandler)
    print(f'Garment extractor backend running at http://localhost:{port}', flush=True)
    print('Press Ctrl+C to stop.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
