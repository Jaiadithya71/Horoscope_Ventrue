"""Place-name lookup via OpenStreetMap Nominatim, throttled to its usage policy.

Returns candidate coordinates for a typed place name. The app always shows the
resolved coordinates for confirmation; coordinates are never guessed silently.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import json
from http.server import BaseHTTPRequestHandler
import time
import urllib.parse
import urllib.request

NOMINATIM_URL = 'https://nominatim.openstreetmap.org/search'
USER_AGENT = 'HoroscopeVentrueResearchPreview/1.0 (local chart research app)'
_last_request_at = 0.0


def _throttle():
    """Nominatim policy: at most one request per second."""
    global _last_request_at
    wait = 1.0 - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    _last_request_at = time.monotonic()


def parse_candidates(payload):
    candidates = []
    for row in payload:
        try:
            lat, lon = float(row['lat']), float(row['lon'])
        except (KeyError, TypeError, ValueError):
            continue
        if not (-90 < lat < 90 and -180 <= lon <= 180):
            continue
        candidates.append({
            'display_name': row.get('display_name', ''),
            'latitude': lat,
            'longitude': lon,
            'category': row.get('category') or row.get('class'),
            'type': row.get('type'),
        })
    return candidates


def geocode(place, limit=5):
    if not isinstance(place, str) or not place.strip():
        raise ValueError('Enter a city, town or state name.')
    if len(place) > 200:
        raise ValueError('Place name is too long.')
    _throttle()
    query = urllib.parse.urlencode({
        'q': place, 'format': 'jsonv2', 'limit': str(limit), 'accept-language': 'en'})
    request = urllib.request.Request(
        f'{NOMINATIM_URL}?{query}', headers={'User-Agent': USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except Exception as exc:
        raise ValueError('Place lookup is unavailable right now. Enter coordinates manually.') from exc
    if not isinstance(payload, list):
        raise ValueError('Place lookup returned an unexpected response. Enter coordinates manually.')
    return parse_candidates(payload)


def response_get(query):
    from urllib.parse import parse_qs
    place = parse_qs(query).get('place', [''])[0]
    try:
        return 200, json.dumps({'candidates': geocode(place)}).encode()
    except ValueError as exc:
        return 400, json.dumps({'error': str(exc)}).encode()


class handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_GET(self):
        from urllib.parse import urlparse
        status, body = response_get(urlparse(self.path).query)
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)
