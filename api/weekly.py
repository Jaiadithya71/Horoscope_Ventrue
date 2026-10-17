"""Thin adapter to engine.weekly_lagna. No invented gates or forecasts."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import datetime as dt
import json
from http.server import BaseHTTPRequestHandler
from engine.weekly_lagna import weekly_lagna_report


def weekly(payload):
    if not isinstance(payload, dict) or set(payload) - {'week_of', 'lagna', 'moon_sign'}:
        raise ValueError('Supply week_of, lagna and optionally moon_sign only.')
    if 'lagna' not in payload:
        raise ValueError('Choose a lagna.')
    try:
        week_of = dt.date.fromisoformat(str(payload.get('week_of', '')))
    except ValueError:
        raise ValueError('week_of must be a YYYY-MM-DD date.')
    moon = payload.get('moon_sign')
    if moon is not None and type(moon) is not str:
        raise ValueError('moon_sign must be a sign name.')
    return weekly_lagna_report(week_of, str(payload['lagna']), moon)


def response_body(raw):
    try:
        if len(raw) > 8192:
            raise ValueError('Request is too large.')
        payload = json.loads(raw)
        data = weekly(payload)
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
