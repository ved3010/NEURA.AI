"""
ULTRON Native macOS Desktop AI Agent Window
===========================================
Runs Sagar Tamang's exact 3D Ultron Orb & MediaPipe UI in a native desktop window.
"""

import sys
import os
import time
import subprocess
import webview

# Import E.D.I.T.H. Engine Tools
from edith.tools.diagnostics import get_system_telemetry, scan_local_network
from edith.tools.protocols import trigger_protocol
from edith.tools.intelligence import search_web
from edith.tools.workspace import analyze_workspace
from edith.memory import remember_fact, recall_memory, add_task, get_tasks


class UltronAgentApi:
    """Native Python API bound directly to the Ultron Desktop UI."""

    def get_telemetry(self):
        return get_system_telemetry()

    def run_protocol(self, name):
        return trigger_protocol(name)

    def scan_network(self):
        return scan_local_network()

    def web_search(self, query):
        return search_web(query)

    def analyze_ws(self):
        return analyze_workspace(".")

    def save_memory(self, key, val):
        return remember_fact(key, val)

    def get_tasks_list(self):
        return get_tasks()


def ensure_nextjs_server():
    """Ensure Ultron Next.js server is active on port 3000."""
    try:
        import urllib.request
        urllib.request.urlopen("http://localhost:3000", timeout=1.5)
        print("[ULTRON] Active on http://localhost:3000")
    except Exception:
        print("[ULTRON] Starting Next.js server...")
        cmd = "PATH=\"/Users/li/evai/node_bin/bin:$PATH\" npm run dev"
        subprocess.Popen(cmd, shell=True, cwd=os.path.abspath("ultron"))
        time.sleep(3)


def main():
    ensure_nextjs_server()
    api = UltronAgentApi()

    # Create native macOS desktop app window pointing directly to Sagar Tamang's Ultron UI
    window = webview.create_window(
        title="ULTRON // Desktop AI Agent",
        url="http://localhost:3000",
        width=1180,
        height=760,
        background_color="#030712",
        resizable=True,
        on_top=True,
        js_api=api
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
