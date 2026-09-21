#!/usr/bin/env python3
"""Serve the built Arduino site locally, with no additional Python packages."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description='Arduino-Webseite lokal starten')
parser.add_argument('--port', type=int, default=5173)
args = parser.parse_args()
root = Path(__file__).resolve().parent / 'dist' / 'client'
if not (root / 'index.html').is_file():
    raise SystemExit('Die gebaute Seite fehlt. Bitte zuerst npm install und npm run build ausführen.')
class Handler(SimpleHTTPRequestHandler):
    extensions_map = {**SimpleHTTPRequestHandler.extensions_map, '.rsc': 'text/x-component'}
    def translate_path(self, path):
        resolved = Path(super().translate_path(path))
        if self.headers.get('RSC') == '1' and not resolved.suffix:
            candidate = resolved / 'index.rsc' if resolved == root else resolved.with_suffix('.rsc')
            if candidate.is_file():
                return str(candidate)
        if not resolved.suffix and resolved.with_suffix('.html').is_file():
            return str(resolved.with_suffix('.html'))
        return str(resolved)
    def __init__(self, *handler_args, **kwargs):
        super().__init__(*handler_args, directory=str(root), **kwargs)
    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()
try:
    with ThreadingHTTPServer(('127.0.0.1', args.port), Handler) as server:
        print(f'\nArduino · Design & Technik\nhttp://127.0.0.1:{args.port}/\n\nZum Beenden: Ctrl+C\n', flush=True)
        server.serve_forever()
except KeyboardInterrupt:
    print('\nWebseite beendet.')
except OSError as error:
    raise SystemExit(f'Der lokale Server konnte nicht starten: {error}\nEin anderer Port ist möglich: python3 serve.py --port 5174')
