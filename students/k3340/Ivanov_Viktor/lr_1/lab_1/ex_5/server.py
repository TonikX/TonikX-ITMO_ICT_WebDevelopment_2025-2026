#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import json
import os
from urllib.parse import parse_qs, urlparse, unquote_plus
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8082
STORAGE_FILE = "grades.json"
TEMPLATE_FILE = "index.html"

grades = {}

def load_storage():
    global grades
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            grades = {str(k): [str(x) for x in v] for k, v in data.items() if isinstance(v, list)}
        except Exception:
            grades = {}
    else:
        grades = {}

def save_storage():
    try:
        with open(STORAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(grades, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def http_response(status_code=200, reason="OK", headers=None, body=b""):
    if headers is None:
        headers = {}
    base_headers = {
        "Server": "TinySocketServer/0.2",
        "Content-Length": str(len(body)),
        "Connection": "close",
        "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
    }
    base_headers.update(headers)
    status_line = f"HTTP/1.1 {status_code} {reason}\r\n"
    header_lines = "".join(f"{k}: {v}\r\n" for k, v in base_headers.items())
    return (status_line + header_lines + "\r\n").encode("utf-8") + body

def escape_html(s: str) -> str:
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;")
             .replace("'", "&#39;"))

def build_table_rows():
    rows = []
    for subj in sorted(grades.keys(), key=lambda s: s.lower()):
        vals = grades[subj]
        joined = ", ".join(vals) if vals else "—"
        avg = "—"
        nums = []
        for v in vals:
            try:
                nums.append(float(v.replace(",", ".")))
            except ValueError:
                pass
        if nums:
            avg = f"{sum(nums) / len(nums):.2f}"
        rows.append(
            f"<tr><td>{escape_html(subj)}</td>"
            f"<td>{escape_html(joined)}</td>"
            f"<td>{avg}</td></tr>"
        )
    if not rows:
        rows = ['<tr><td colspan="3" style="text-align:center;color:#666">'
                'Пока пусто. Добавьте первую оценку ниже 👇</td></tr>']
    return "\n".join(rows)

def render_html_from_file():
    try:
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
            tpl = f.read()
    except FileNotFoundError:
        # fallback: если шаблон потерян
        return "<h1>Шаблон index.html не найден</h1>".encode("utf-8")

    page = (tpl
            .replace("{{TABLE_ROWS}}", build_table_rows())
            .replace("{{NOW}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return page.encode("utf-8")

def parse_request_line(request_line: str):
    parts = request_line.split()
    if len(parts) != 3:
        raise ValueError("Malformed request line")
    method, target, version = parts
    if not version.startswith("HTTP/"):
        raise ValueError("Unsupported HTTP version")
    return method.upper(), target, version

def handle_client(conn, addr):
    try:
        request_data = b""
        while b"\r\n\r\n" not in request_data:
            chunk = conn.recv(4096)
            if not chunk:
                break
            request_data += chunk

        if not request_data:
            conn.sendall(http_response(400, "Bad Request",
                                       headers={"Content-Type": "text/plain; charset=utf-8"},
                                       body=b"Bad Request"))
            return

        header_part, _, rest = request_data.partition(b"\r\n\r\n")
        try:
            header_text = header_part.decode("iso-8859-1", errors="replace")
        except Exception:
            header_text = header_part.decode("utf-8", errors="replace")

        lines = header_text.split("\r\n")
        request_line = lines[0]
        method, target, version = parse_request_line(request_line)

        headers = {}
        for line in lines[1:]:
            if not line:
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip().lower()] = v.strip()

        body = rest
        content_length = int(headers.get("content-length", "0") or "0")
        to_read = max(0, content_length - len(body))
        while to_read > 0:
            chunk = conn.recv(min(4096, to_read))
            if not chunk:
                break
            body += chunk
            to_read -= len(chunk)

        parsed = urlparse(target)
        path = parsed.path

        # GET /
        if method == "GET" and path == "/":
            body_bytes = render_html_from_file()
            conn.sendall(http_response(200, "OK",
                                       headers={"Content-Type": "text/html; charset=utf-8"},
                                       body=body_bytes))
            return

        # GET /api/grades
        if method == "GET" and path == "/api/grades":
            body_bytes = json.dumps(grades, ensure_ascii=False, indent=2).encode("utf-8")
            conn.sendall(http_response(200, "OK",
                                       headers={"Content-Type": "application/json; charset=utf-8"},
                                       body=body_bytes))
            return

        # POST /add
        if method == "POST" and path == "/add":
            ctype = headers.get("content-type", "")
            payload = body.decode("utf-8", errors="replace")
            form = parse_qs(payload, keep_blank_values=True) if "application/x-www-form-urlencoded" in ctype else parse_qs(payload, keep_blank_values=True)

            subject = unquote_plus(form.get("subject", [""])[0].strip())
            grade = unquote_plus(form.get("grade", [""])[0].strip())

            if not subject or not grade:
                msg = "Both 'subject' and 'grade' are required."
                conn.sendall(http_response(400, "Bad Request",
                                           headers={"Content-Type": "text/plain; charset=utf-8"},
                                           body=msg.encode("utf-8")))
                return

            if subject not in grades:
                grades[subject] = []
            grades[subject].append(grade)
            save_storage()

            # redirect back to /
            conn.sendall(http_response(303, "See Other",
                                       headers={"Location": "/", "Content-Type": "text/plain; charset=utf-8"},
                                       body=b"See Other"))
            return

        # unsupported
        if method not in ("GET", "POST"):
            conn.sendall(http_response(405, "Method Not Allowed",
                                       headers={"Content-Type": "text/plain; charset=utf-8",
                                                "Allow": "GET, POST"},
                                       body=b"Method Not Allowed"))
            return

        conn.sendall(http_response(404, "Not Found",
                                   headers={"Content-Type": "text/plain; charset=utf-8"},
                                   body=b"Not Found"))
    except Exception as e:
        try:
            conn.sendall(http_response(500, "Internal Server Error",
                                       headers={"Content-Type": "text/plain; charset=utf-8"},
                                       body=f"Internal Server Error: {e}".encode("utf-8")))
        except Exception:
            pass
    finally:
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        conn.close()

def serve():
    load_storage()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(128)
        print(f"Serving on http://{HOST}:{PORT} …")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    serve()
