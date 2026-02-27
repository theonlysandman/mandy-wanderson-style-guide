"""
Style Agent – Local server with file upload support.
Run:  python server.py
Then open http://localhost:8123
"""

import http.server
import json
import os
import uuid
import cgi
from pathlib import Path

PORT = 8123
BASE = Path(__file__).parent
UPLOADS = BASE / "uploads"
WARDROBE_FILE = BASE / "wardrobe.json"

UPLOADS.mkdir(exist_ok=True)


def load_wardrobe():
    if WARDROBE_FILE.exists():
        return json.loads(WARDROBE_FILE.read_text(encoding="utf-8"))
    return None


def save_wardrobe(data):
    WARDROBE_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)

    def do_POST(self):
        if self.path == "/api/upload":
            self._handle_upload()
        elif self.path == "/api/wardrobe":
            self._handle_save_wardrobe()
        elif self.path == "/api/face":
            self._handle_face_upload()
        else:
            self.send_error(404)

    def do_GET(self):
        if self.path == "/api/wardrobe":
            self._handle_get_wardrobe()
        else:
            super().do_GET()

    # ---- Upload a clothing photo ----
    def _handle_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_error(400, "Expected multipart/form-data")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type},
        )

        file_item = form["file"]
        if file_item.filename:
            ext = Path(file_item.filename).suffix or ".jpg"
            filename = f"{uuid.uuid4().hex[:10]}{ext}"
            filepath = UPLOADS / filename
            filepath.write_bytes(file_item.file.read())

            self._json_response({"path": f"uploads/{filename}"})
        else:
            self.send_error(400, "No file provided")

    # ---- Upload face photo ----
    def _handle_face_upload(self):
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_error(400, "Expected multipart/form-data")
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={"REQUEST_METHOD": "POST", "CONTENT_TYPE": content_type},
        )

        file_item = form["file"]
        if file_item.filename:
            ext = Path(file_item.filename).suffix or ".jpg"
            filename = f"face{ext}"
            filepath = UPLOADS / filename
            filepath.write_bytes(file_item.file.read())

            self._json_response({"path": f"uploads/{filename}"})
        else:
            self.send_error(400, "No file provided")

    # ---- Save wardrobe JSON ----
    def _handle_save_wardrobe(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        data = json.loads(body)
        save_wardrobe(data)
        self._json_response({"ok": True})

    # ---- Load wardrobe JSON ----
    def _handle_get_wardrobe(self):
        data = load_wardrobe()
        if data is None:
            self._json_response(None)
        else:
            self._json_response(data)

    def _json_response(self, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print(f"Style Agent server running at http://localhost:{PORT}")
    with http.server.HTTPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
