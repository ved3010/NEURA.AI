"""
E.D.I.T.H. Native Desktop Application (macOS WebKit Overlay)
Runs the futuristic E.D.I.T.H. Tactical HUD in a native desktop window with Python backend API binding.
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


class EdithApi:
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
    api = EdithApi()
    html_path = os.path.abspath("hud/index.html")
    
    window = webview.create_window(
        title="E.D.I.T.H. — Tactical AI Overlay",
        url=f"file://{html_path}",
        width=1100,
        height=720,
        resizable=True,
        on_top=True,
        js_api=api
    )
    
    webview.start(debug=False)


if __name__ == "__main__":
    main()
