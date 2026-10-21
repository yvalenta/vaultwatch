"""The operated system: a toy endpoint the vault describes.

Reads world/served.json on every request, so changing that file is "the world
moving" without anybody touching the docs.

    python3 server.py PORT
"""
import http.server
import json
import pathlib
import sys

SERVED = pathlib.Path(__file__).resolve().parent / "served.json"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        data = json.loads(SERVED.read_text())
        if self.path == "/price":
            body = {"price_usd": data["price_usd"]}
        elif self.path == "/requests":
            body = {"requests_today": data["requests_today"]}
        else:
            self.send_error(404)
            return
        payload = json.dumps(body).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    http.server.HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
