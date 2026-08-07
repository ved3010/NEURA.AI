"""
E.D.I.T.H. Floating Desktop AI Widget (macOS / Desktop Overlay)
"Even In Death, I'm The Hero" — Floating Arc Reactor Desktop Assistant

Features:
• Always-on-top frameless transparent floating orb widget.
• Draggable across screen.
• Pulse-glowing Arc Reactor visualizer.
• Expandable command input bar & tactical protocol triggers.
• Real-time speech & E.D.I.T.H. tool execution output.
"""

import sys
import os
import time
import math
from PySide6.QtCore import Qt, QTimer, QPoint, QRectF, Signal, QThread
from PySide6.QtGui import QPainter, QColor, QRadialGradient, QPen, QFont, QBrush, QPainterPath
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QLabel, QGraphicsDropShadowEffect, QFrame
)

# Import E.D.I.T.H. Engine Tools
from edith.tools.diagnostics import get_system_telemetry, scan_local_network
from edith.tools.protocols import trigger_protocol
from edith.tools.intelligence import search_web
from edith.tools.workspace import analyze_workspace, run_terminal_command
from edith.memory import remember_fact, recall_memory, add_task, get_tasks


class ToolWorker(QThread):
    finished = Signal(str)

    def __init__(self, command_text):
        super().__init__()
        self.command_text = command_text

    def run(self):
        cmd = self.command_text.strip().lower()
        if "diagnostic" in cmd or "telemetry" in cmd or "system" in cmd:
            res = get_system_telemetry()
        elif "protocol" in cmd:
            res = trigger_protocol(cmd)
        elif "network" in cmd or "radar" in cmd:
            res = scan_local_network()
        elif "search" in cmd or "web" in cmd or "news" in cmd:
            res = search_web(cmd.replace("search", "").replace("web", "").strip() or "breaking world news")
        elif "workspace" in cmd or "code" in cmd:
            res = analyze_workspace(".")
        elif "remember" in cmd:
            parts = cmd.replace("remember", "").strip().split(":", 1)
            key = parts[0] if parts else "note"
            val = parts[1] if len(parts) > 1 else parts[0]
            res = remember_fact(key, val)
        elif "task" in cmd:
            if "add" in cmd:
                res = add_task(cmd.replace("add task", "").replace("task", "").strip())
            else:
                res = get_tasks()
        else:
            res = f"E.D.I.T.H. Matrix Response: Acknowledged command '{self.command_text}'. All systems nominal, boss."

        self.finished.emit(res)


class ArcReactorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(140, 140)
        self.angle = 0.0
        self.pulse = 1.0
        self.pulse_dir = 0.02
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle += 0.03
        self.pulse += self.pulse_dir
        if self.pulse > 1.15 or self.pulse < 0.85:
            self.pulse_dir *= -1
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = self.width() / 2, self.height() / 2

        # Outer Glow
        glow = QRadialGradient(cx, cy, 65)
        glow.setColorAt(0, QColor(0, 240, 255, 160))
        glow.setColorAt(0.5, QColor(0, 150, 255, 60))
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(5, 5, 130, 130)

        # Outer Arc Ring
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(math.degrees(self.angle))

        pen = QPen(QColor(0, 240, 255), 2.5)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawArc(QRectF(-48, -48, 96, 96), 0, 270 * 16)
        painter.restore()

        # Inner Counter Ring
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(-math.degrees(self.angle * 1.5))
        pen2 = QPen(QColor(0, 81, 255), 3)
        painter.setPen(pen2)
        painter.drawArc(QRectF(-36, -36, 72, 72), 0, 200 * 16)
        painter.restore()

        # Core Pulsing Circle
        r = 22 * self.pulse
        core_grad = QRadialGradient(cx, cy, r)
        core_grad.setColorAt(0, QColor(255, 255, 255, 240))
        core_grad.setColorAt(0.4, QColor(0, 240, 255, 220))
        core_grad.setColorAt(1, QColor(0, 81, 255, 100))
        painter.setBrush(QBrush(core_grad))
        painter.setPen(QPen(QColor(0, 240, 255), 1.5))
        painter.drawEllipse(QRectF(cx - r, cy - r, r * 2, r * 2))

        # E.D.I.T.H. Label
        font = QFont("Helvetica", 8, QFont.Bold)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(QRectF(0, cy + 30, 140, 20), Qt.AlignCenter, "E.D.I.T.H.")


class EdithFloatingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = QPoint()
        self.expanded = False

        # Window Flags: Frameless, Always-On-Top, Translucent Background
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.SubWindow
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(6)

        # Header Container with Arc Reactor
        self.header = QFrame(self)
        self.header.setStyleSheet("""
            QFrame {
                background: rgba(3, 10, 24, 0.85);
                border: 1px solid rgba(0, 240, 255, 0.35);
                border-radius: 20px;
            }
        """)

        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 6, 12, 6)

        # Arc Reactor Orb
        self.reactor = ArcReactorWidget(self)
        header_layout.addWidget(self.reactor)

        # Right Info & Quick Action Bar
        info_layout = QVBoxLayout()
        title_label = QLabel("E.D.I.T.H.", self)
        title_label.setStyleSheet("color: #00f0ff; font-weight: bold; font-size: 16px; font-family: Helvetica;")
        sub_label = QLabel("STARK AI DESKTOP OVERLAY", self)
        sub_label.setStyleSheet("color: #648ba6; font-size: 9px; font-family: Helvetica;")

        info_layout.addWidget(title_label)
        info_layout.addWidget(sub_label)

        # Protocol Button Row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(4)

        for p_name, p_label in [("edith", "EDITH"), ("sentry", "SENTRY"), ("stealth", "STEALTH"), ("overclock", "BOOST")]:
            btn = QPushButton(p_label, self)
            btn.setFixedSize(56, 22)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(0, 240, 255, 0.12);
                    border: 1px solid rgba(0, 240, 255, 0.3);
                    border-radius: 4px;
                    color: #00f0ff;
                    font-size: 9px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: rgba(0, 240, 255, 0.35);
                    color: #ffffff;
                }
            """)
            btn.clicked.connect(lambda checked, name=p_name: self.run_quick_protocol(name))
            btn_layout.addWidget(btn)

        info_layout.addLayout(btn_layout)
        header_layout.addLayout(info_layout)

        main_layout.addWidget(self.header)

        # Command Input Bar
        self.input_bar = QLineEdit(self)
        self.input_bar.setPlaceholderText("Ask E.D.I.T.H. or enter command...")
        self.input_bar.setStyleSheet("""
            QLineEdit {
                background: rgba(2, 6, 16, 0.9);
                border: 1px solid rgba(0, 240, 255, 0.4);
                border-radius: 12px;
                padding: 8px 12px;
                color: #e2f1ff;
                font-size: 12px;
                font-family: Helvetica;
            }
            QLineEdit:focus {
                border-color: #00f0ff;
            }
        """)
        self.input_bar.returnPressed.connect(self.submit_command)
        main_layout.addWidget(self.input_bar)

        # AI Response Display Bubble
        self.response_box = QLabel("E.D.I.T.H. online, boss. Ready on desktop overlay.", self)
        self.response_box.setWordWrap(True)
        self.response_box.setStyleSheet("""
            QLabel {
                background: rgba(7, 16, 38, 0.9);
                border: 1px solid rgba(0, 240, 255, 0.25);
                border-radius: 12px;
                padding: 10px 14px;
                color: #00f0ff;
                font-size: 11px;
                font-family: Helvetica;
            }
        """)
        main_layout.addWidget(self.response_box)

        self.adjustSize()

    # Enable Window Dragging by clicking anywhere on header
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def run_quick_protocol(self, p_name):
        self.response_box.setText(f"[E.D.I.T.H.] Initiating Protocol '{p_name.upper()}'...")
        res = trigger_protocol(p_name)
        self.response_box.setText(res)

    def submit_command(self):
        cmd = self.input_bar.text().strip()
        if not cmd:
            return
        self.input_bar.clear()
        self.response_box.setText(f"[USER] {cmd}\n[E.D.I.T.H.] Processing query...")

        # Run tool in background thread
        self.worker = ToolWorker(cmd)
        self.worker.finished.connect(self.on_tool_finished)
        self.worker.start()

    def on_tool_finished(self, result_text):
        self.response_box.setText(f"[E.D.I.T.H.] {result_text}")


def main():
    app = QApplication(sys.argv)
    widget = EdithFloatingWidget()
    widget.move(100, 100)
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
