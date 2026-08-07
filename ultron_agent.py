"""
ULTRON // E.D.I.T.H. Native macOS Desktop AI Agent
==================================================
Native desktop application window (no browser tabs/URLs) featuring the 3D Holographic Orb,
MediaPipe hand gesture tracking, and E.D.I.T.H. backend tool intelligence.
"""

import sys
import os
import webview

# Import E.D.I.T.H. Engine Tools
from edith.tools.diagnostics import get_system_telemetry, scan_local_network
from edith.tools.protocols import trigger_protocol
from edith.tools.intelligence import search_web
from edith.tools.workspace import analyze_workspace
from edith.memory import remember_fact, recall_memory, add_task, get_tasks


class UltronAgentApi:
    """Native Python API bound directly to the Desktop AI Agent UI."""

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


def main():
    api = UltronAgentApi()
    
    # Absolute path to local html file
    html_file = os.path.abspath("hud/index.html")

    # Create native macOS desktop application window (no browser UI)
    window = webview.create_window(
        title="ULTRON // Desktop AI Agent",
        url=f"file://{html_file}",
        width=1120,
        height=740,
        resizable=True,
        on_top=True,
        js_api=api
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
