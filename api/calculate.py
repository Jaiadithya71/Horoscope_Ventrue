"""Thin, strict adapter to the existing engine. No forecasts or invented gates."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from http.server import BaseHTTPRequestHandler
from engine.research_input_report import research_input_report

def calculate(payload):
    if not isinstance(payload, dict) or set(payload) != {'birth'}:
        raise ValueError('Supply birth details only.')
    birth = payload['birth']
    # The engine owns exact fields, clock validation, coordinate checks and math.
    report = research_input_report(birth)
    # Phone-first payload: the app never reads the raw per-planet factor tables
    # (about 0.9 MB). The engine still computes them; only the HTTP response omits them.
    chart = report.get('natal_chart')
    if isinstance(chart, dict):
        report = {**report, 'natal_chart': {k: v for k, v in chart.items() if k != 'natal_factors'}}
    return report

def response_body(raw):
    try:
        if len(raw) > 8192:
            raise ValueError('Request is too large.')
        payload = json.loads(raw)
        data = calculate(payload)
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
