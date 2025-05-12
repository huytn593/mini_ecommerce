#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os
import sys

PORT = 3000
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_ROOT, **kwargs)

    def translate_path(self, path):
        # Đối với các yêu cầu bắt đầu bằng /static/, sử dụng thư mục gốc dự án
        if path.startswith('/static/'):
            return os.path.join(PROJECT_ROOT, path.lstrip('/'))
        # Đối với các yêu cầu khác, sử dụng thư mục frontend
        else:
            path = super().translate_path(path)
            rel_path = os.path.relpath(path, self.directory)
            return os.path.join(DIRECTORY, rel_path)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()


def run():
    print(f"Serving frontend at http://localhost:{PORT}")
    print(f"Project root: {PROJECT_ROOT}")
    print(f"Frontend directory: {DIRECTORY}")
    httpd = socketserver.TCPServer(("", PORT), Handler)
    httpd.serve_forever()


if __name__ == "__main__":
    run()