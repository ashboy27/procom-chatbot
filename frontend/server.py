from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 3001
BASE_DIR = Path(__file__).resolve().parent


class FrontendHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)


if __name__ == "__main__":
    print(f"Serving frontend on http://localhost:{PORT}")
    ThreadingHTTPServer(("0.0.0.0", PORT), FrontendHandler).serve_forever()
