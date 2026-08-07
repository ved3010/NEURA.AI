"""
ULTRON // E.D.I.T.H. Desktop AI Application Window
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


class UltronEdithApi:
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
    api = UltronEdithApi()

    # Create native macOS desktop app window
    window = webview.create_window(
        title="ULTRON // E.D.I.T.H. Desktop AI",
        url="http://localhost:3000",
        width=1100,
        height=720,
        resizable=True,
        on_top=True,
        js_api=api
    )

    webview.start(debug=False)


if __name__ == "__main__":
    main()
