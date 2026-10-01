"""Local research preview. No birth details are written to disk or logged."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from api.calculate import calculate, response_body

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    def log_message(self, *args):
        pass
    def do_POST(self):
        if self.path != '/api/calculate':
            self.send_error(404); return
        length = int(self.headers.get('Content-Length', 0))
        if length > 8192:
            self.send_error(413); return
        status, data = response_body(self.rfile.read(length))
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.end_headers(); self.wfile.write(data)

if __name__ == '__main__':
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
