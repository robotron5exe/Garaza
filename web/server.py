#!/usr/bin/env python3
"""
Simple HTTP server for the real estate website.

Usage:
    python server.py [port]

Default port is 8000.
"""

import sys
import http.server
import socketserver
from pathlib import Path

# Get port from command line or use default
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

# Change to web directory
web_dir = Path(__file__).parent
import os
os.chdir(web_dir)

# Create handler
Handler = http.server.SimpleHTTPRequestHandler

# Create server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("=" * 70)
    print("MARIBOR REAL ESTATE WEBSITE SERVER")
    print("=" * 70)
    print(f"\n🌐 Server running at: http://localhost:{PORT}")
    print(f"📂 Serving directory: {web_dir}")
    print(f"\n📊 Open http://localhost:{PORT} in your browser")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    print()

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        sys.exit(0)
