"""
E.D.I.T.H. Native Desktop Floating AI Widget (macOS Overlay)
Always-On-Top, Draggable Arc Reactor Assistant for Desktop.
"""

import sys
import os
import math
import subprocess
import tkinter as tk
from tkinter import ttk
import threading

# Import E.D.I.T.H. Engine Tools
from edith.tools.diagnostics import get_system_telemetry, scan_local_network
from edith.tools.protocols import trigger_protocol
from edith.tools.intelligence import search_web
from edith.tools.workspace import analyze_workspace
from edith.memory import remember_fact, recall_memory, add_task, get_tasks


def force_bring_to_front(root):
    """Force Python Tkinter window to front on macOS."""
    try:
        pid = os.getpid()
        cmd = f"osascript -e 'tell application \"System Events\" to set frontmost of (first process whose unix id is {pid}) to true'"
        subprocess.run(cmd, shell=True, capture_output=True)
    except Exception:
        pass


class EdithFloatingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E.D.I.T.H. Desktop AI")
        
        # Window attributes: Always On Top
        self.root.wm_attributes("-topmost", True)
        self.root.configure(bg="#030a18")
        
        # Default geometry & position on upper-right screen
        screen_w = self.root.winfo_screenwidth()
        x_pos = max(100, screen_w - 420)
        self.root.geometry(f"380x320+{x_pos}+120")

        self.angle = 0.0
        self.setup_ui()
        self.animate_reactor()

        # Lift & Bring to front
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after(200, lambda: force_bring_to_front(self.root))

    def setup_ui(self):
        # Outer Border Frame
        self.outer_frame = tk.Frame(self.root, bg="#030a18", highlightbackground="#00f0ff", highlightthickness=2)
        self.outer_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Top Header Bar
        top_bar = tk.Frame(self.outer_frame, bg="#071426")
        top_bar.pack(fill=tk.X, padx=5, pady=5)

        # Arc Reactor Canvas
        self.canvas = tk.Canvas(top_bar, width=54, height=54, bg="#071426", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, padx=5)

        # Title Label Group
        title_frame = tk.Frame(top_bar, bg="#071426")
        title_frame.pack(side=tk.LEFT, padx=5)

        lbl_title = tk.Label(title_frame, text="E.D.I.T.H.", font=("Helvetica", 14, "bold"), fg="#00f0ff", bg="#071426")
        lbl_title.pack(anchor="w")
        lbl_sub = tk.Label(title_frame, text="STARK AI DESKTOP OVERLAY", font=("Helvetica", 8), fg="#648ba6", bg="#071426")
        lbl_sub.pack(anchor="w")

        # Quick Protocol Buttons Row
        proto_bar = tk.Frame(self.outer_frame, bg="#030a18")
        proto_bar.pack(fill=tk.X, padx=8, pady=4)

        protocols = [("EDITH", "edith"), ("SENTRY", "sentry"), ("STEALTH", "stealth"), ("BOOST", "overclock")]
        for label, name in protocols:
            btn = tk.Button(
                proto_bar, text=label, font=("Helvetica", 8, "bold"),
                fg="#00f0ff", bg="#0a1c36", activebackground="#00f0ff", activeforeground="#000000",
                bd=1, relief=tk.FLAT, command=lambda n=name: self.run_protocol(n)
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        # AI Response Display Bubble
        self.lbl_response = tk.Label(
            self.outer_frame, text="[E.D.I.T.H.] Floating AI Desktop Overlay online, boss.",
            font=("Helvetica", 9), fg="#00f0ff", bg="#08182d", justify=tk.LEFT,
            wraplength=340, anchor="nw", padx=8, pady=8, height=7
        )
        self.lbl_response.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        # Command Input Bar
        input_frame = tk.Frame(self.outer_frame, bg="#030a18")
        input_frame.pack(fill=tk.X, padx=8, pady=6)

        self.entry_cmd = tk.Entry(
            input_frame, font=("Helvetica", 10), fg="#00f0ff", bg="#020712",
            insertbackground="#00f0ff", bd=1, relief=tk.SOLID
        )
        self.entry_cmd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        self.entry_cmd.bind("<Return>", lambda e: self.submit_command())

        btn_send = tk.Button(
            input_frame, text="SEND", font=("Helvetica", 8, "bold"),
            fg="#000000", bg="#00f0ff", activebackground="#ffffff",
            bd=0, padx=10, command=self.submit_command
        )
        btn_send.pack(side=tk.RIGHT)

    def animate_reactor(self):
        self.canvas.delete("all")
        cx, cy = 27, 27
        r1, r2 = 20, 14

        pulse = 1.0 + 0.15 * math.sin(self.angle * 2)
        r_pulse = r2 * pulse
        self.canvas.create_oval(cx - r_pulse, cy - r_pulse, cx + r_pulse, cy + r_pulse, fill="#0051ff", outline="#00f0ff", width=1.5)

        x1 = cx + r1 * math.cos(self.angle)
        y1 = cy + r1 * math.sin(self.angle)
        x2 = cx + r1 * math.cos(self.angle + 2.5)
        y2 = cy + r1 * math.sin(self.angle + 2.5)
        self.canvas.create_line(x1, y1, x2, y2, fill="#00f0ff", width=3)

        self.canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="#ffffff", outline="#00f0ff")

        self.angle += 0.08
        self.root.after(40, self.animate_reactor)

    def run_protocol(self, p_name):
        self.lbl_response.config(text=f"[E.D.I.T.H.] Initiating Protocol '{p_name.upper()}'...")
        res = trigger_protocol(p_name)
        self.lbl_response.config(text=res)

    def submit_command(self):
        cmd = self.entry_cmd.get().strip()
        if not cmd:
            return
        self.entry_cmd.delete(0, tk.END)
        self.lbl_response.config(text=f"[USER] {cmd}\n[E.D.I.T.H.] Querying system...")

        threading.Thread(target=self._worker_task, args=(cmd,), daemon=True).start()

    def _worker_task(self, cmd):
        c = cmd.lower()
        if "diagnostic" in c or "telemetry" in c or "system" in c:
            res = get_system_telemetry()
        elif "protocol" in c:
            res = trigger_protocol(c)
        elif "network" in c or "radar" in c:
            res = scan_local_network()
        elif "search" in c or "web" in c or "news" in c:
            res = search_web(c.replace("search", "").replace("web", "").strip() or "breaking news")
        elif "workspace" in c or "code" in c:
            res = analyze_workspace(".")
        elif "remember" in c:
            parts = c.replace("remember", "").strip().split(":", 1)
            key = parts[0] if parts else "note"
            val = parts[1] if len(parts) > 1 else parts[0]
            res = remember_fact(key, val)
        elif "task" in c:
            if "add" in c:
                res = add_task(c.replace("add task", "").replace("task", "").strip())
            else:
                res = get_tasks()
        else:
            res = f"E.D.I.T.H. Response: Command '{cmd}' processed. Subsystems nominal."

        self.root.after(0, lambda: self.lbl_response.config(text=f"[E.D.I.T.H.] {res}"))


def main():
    root = tk.Tk()
    app = EdithFloatingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
