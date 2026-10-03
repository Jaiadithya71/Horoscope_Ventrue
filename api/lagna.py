"""Lagna options for an uncertain birth time. Arithmetic only; no forecast."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from http.server import BaseHTTPRequestHandler
from engine.lagna_options import lagna_spans, lagna_for_known_sign

KEYS = {'date', 'timezone', 'latitude', 'longitude'}

def options(payload):
    if not isinstance(payload, dict):
        raise ValueError('Supply the birth date, place and either a time window or a known lagna.')
    mode = payload.get('mode')
    base = {k: payload.get(k) for k in KEYS}
    if mode == 'window':
        if set(payload) != KEYS | {'mode', 'start', 'end'}:
            raise ValueError('Window mode needs date, timezone, latitude, longitude, start and end.')
        return lagna_spans(**base, start=payload['start'], end=payload['end'])
    if mode == 'known':
        if not set(payload) <= KEYS | {'mode', 'lagna', 'around'} or 'lagna' not in payload:
            raise ValueError('Known-lagna mode needs date, timezone, latitude, longitude and lagna.')
        return lagna_for_known_sign(**base, lagna=payload['lagna'], around=payload.get('around') or None)
    raise ValueError('Unknown mode.')

def response_body(raw):
    try:
        if len(raw) > 4096:
            raise ValueError('Request is too large.')
        return 200, json.dumps(options(json.loads(raw)), allow_nan=False).encode()
    except (ValueError, TypeError, KeyError) as exc:
        return 400, json.dumps({'error': str(exc)}).encode()
    except Exception:
        return 503, json.dumps({'error': 'Lagna options are unavailable.'}).encode()

class handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            length = 4097
        if length > 4096:
            self.send_response(413); self.end_headers(); return
        status, body = response_body(self.rfile.read(length))
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers(); self.wfile.write(body)
