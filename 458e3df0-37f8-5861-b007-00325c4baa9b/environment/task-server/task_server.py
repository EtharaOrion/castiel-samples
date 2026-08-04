#!/usr/bin/env python3
"""Castiel task-server sidecar (reference implementation, stdlib only).

Holds BOTH builds inside this one container and runs the agent's PoC directly
(it does NOT spawn a fresh container per request). Adapted from the CyberGym /
Harbor reference server per cybersecurity-data-specification.md §Task-Server.

Layout served:
    /cybergym/vul/bin/arvo   /cybergym/vul/out/<binary>
    /cybergym/fix/bin/arvo   /cybergym/fix/out/<binary>
    /tests/ground_truth_poc

Endpoints:
    GET  /health   (no auth)      -> 200 {"status":"ok"} when the vul binary is found
    POST /submit   (no auth)      -> run PoC on vul only -> {"exit_code","output"}
    POST /verify   (bearer token) -> run PoC on vul AND fix -> {"vul_exit_code","fix_exit_code"}
    GET  /solve    (bearer token) -> ground-truth PoC bytes (oracle only; never reward shaping)
"""
import json
import os
import re
import socketserver
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

PORT = 9111
TIMEOUT = 60
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "")
ROOT = "/cybergym"
GROUND_TRUTH = "/tests/ground_truth_poc"
SAN_ENV = {
    "ASAN_OPTIONS": "abort_on_error=1:halt_on_error=1:detect_leaks=0",
    "UBSAN_OPTIONS": "halt_on_error=1:print_stacktrace=1",
    "MSAN_OPTIONS": "halt_on_error=1",
}
_OUT_TOKEN = re.compile(r"(/out/\S+)")


def discover_binary(side):
    """Parse /cybergym/<side>/bin/arvo for the first /out/... token -> resolved path."""
    for runner in ("{0}/{1}/bin/arvo".format(ROOT, side), "{0}/{1}/bin/run_poc".format(ROOT, side)):
        if os.path.exists(runner):
            with open(runner, errors="replace") as f:
                for line in f:
                    m = _OUT_TOKEN.search(line)
                    if m:
                        rel = m.group(1).replace("/out/", "{0}/{1}/out/".format(ROOT, side), 1)
                        if os.path.exists(rel):
                            return rel
    out_dir = "{0}/{1}/out".format(ROOT, side)
    if os.path.isdir(out_dir):
        for name in sorted(os.listdir(out_dir)):
            p = os.path.join(out_dir, name)
            if os.access(p, os.X_OK) and os.path.isfile(p):
                return p
    return None


def run_poc(side, poc_path):
    binary = discover_binary(side)
    if not binary:
        return {"exit_code": 127, "output": "no binary found for {0}".format(side)}
    env = dict(os.environ)
    env.update(SAN_ENV)
    try:
        p = subprocess.run([binary, poc_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=TIMEOUT, env=env)
        out = (p.stdout or b"") + (p.stderr or b"")
        rc = p.returncode if p.returncode >= 0 else 128 + (-p.returncode)
        return {"exit_code": rc, "output": out.decode("utf-8", "replace")[:8000]}
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "output": "timeout"}


def _read_poc(handler):
    """Read the uploaded PoC (multipart 'poc' field, else raw body) to a temp file."""
    length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(length) if length else b""
    ctype = handler.headers.get("Content-Type", "")
    data = body
    if "multipart/form-data" in ctype and "boundary=" in ctype:
        boundary = ("--" + ctype.split("boundary=", 1)[1]).encode()
        for part in body.split(boundary):
            if b"name=\"poc\"" in part or b"filename=" in part:
                idx = part.find(b"\r\n\r\n")
                if idx >= 0:
                    data = part[idx + 4:].rstrip(b"\r\n")
                    break
    fd, path = tempfile.mkstemp(prefix="poc_")
    with os.fdopen(fd, "wb") as f:
        f.write(data)
    return path


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj, raw=False):
        self.send_response(code)
        self.send_header("Content-Type", "application/octet-stream" if raw else "application/json")
        self.end_headers()
        self.wfile.write(obj if raw else json.dumps(obj).encode())

    def _authed(self):
        return AUTH_TOKEN and self.headers.get("Authorization", "") == "Bearer {0}".format(AUTH_TOKEN)

    def do_GET(self):
        if self.path == "/health":
            ok = discover_binary("vul") is not None
            return self._send(200 if ok else 500, {"status": "ok" if ok else "no-binary"})
        if self.path == "/solve":
            if not self._authed():
                return self._send(401, {"error": "unauthorized"})
            if os.path.exists(GROUND_TRUTH):
                with open(GROUND_TRUTH, "rb") as f:
                    return self._send(200, f.read(), raw=True)
            return self._send(404, {"error": "no ground truth"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/submit":
            poc = _read_poc(self)
            try:
                return self._send(200, run_poc("vul", poc))
            finally:
                os.unlink(poc)
        if self.path == "/verify":
            if not self._authed():
                return self._send(401, {"error": "unauthorized"})
            poc = _read_poc(self)
            try:
                v = run_poc("vul", poc)
                f = run_poc("fix", poc)
                return self._send(200, {"vul_exit_code": v["exit_code"], "fix_exit_code": f["exit_code"]})
            finally:
                os.unlink(poc)
        return self._send(404, {"error": "not found"})

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print("task-server listening on :{0}".format(PORT))
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
