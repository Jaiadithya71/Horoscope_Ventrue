"""Thin adapter to engine.content_studio. No invented rules or readings."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from http.server import BaseHTTPRequestHandler
from engine.content_studio import studio_report, studio_index, TOOLS


def studio(payload):
    if not isinstance(payload, dict) or set(payload) - {'tool', 'choice'}:
        raise ValueError('Supply tool and choice only.')
    if payload.get('tool') == 'index':
        return studio_index()
    if payload.get('tool') not in TOOLS:
        raise ValueError('Unknown tool.')
    if 'choice' not in payload:
        raise ValueError('Pick a choice.')
    return studio_report(payload['tool'], payload['choice'])


def response_body(raw):
    try:
        if len(raw) > 8192:
            raise ValueError('Request is too large.')
        payload = json.loads(raw)
        data = studio(payload)
        return 200, json.dumps(data, allow_nan=False).encode()
    except (ValueError, TypeError, KeyError) as exc:
        return 400, json.dumps({'error': str(exc)}).encode()
    except Exception:
        return 503, json.dumps({'error': 'Calculation is unavailable. No result has been generated.'}).encode()


class handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            length = 8193
        if length > 8192:
            self.send_response(413); self.end_headers(); return
        status, body = response_body(self.rfile.read(length))
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers(); self.wfile.write(body)
