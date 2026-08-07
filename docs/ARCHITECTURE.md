# E.D.I.T.H. & Ultron Architecture Reference Guide

This document describes the high-level system architecture, MCP tool integrations, 3D WebGL renderer, and LiveKit voice streaming architecture for **E.D.I.T.H. v2.0**.

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          E.D.I.T.H. TACTICAL AI                             │
└──────────────────────┬───────────────────────────────┬──────────────────────┘
                       │                               │
                       ▼                               ▼
       ┌───────────────────────────────┐     ┌────────────────────────────────┐
       │   FastMCP Tool Server (:8000) │     │ 3D Holographic UI / Desktop    │
       ├───────────────────────────────┤     ├────────────────────────────────┤
       │ • System Telemetry            │     │ • Three.js 3D Holographic Core │
       │ • Stark Protocols             │     │ • MediaPipe Hand Tracker       │
       │ • Autonomous Web Search       │     │ • Native macOS Desktop Overlay │
       │ • Workspace Analyzer          │     │ • Interactive Command Terminal │
       │ • Persistent Memory Store     │     └────────────────────────────────┘
       └───────────────────────────────┘
```

---

## Core Component Modules

### 1. FastMCP Tool Server (`server.py`)
Exposes JSON-RPC & SSE endpoints at `http://127.0.0.1:8000/sse`. 

### 2. LiveKit Tactical Voice Agent (`agent_edith.py`)
Streams real-time audio via WebRTC.
- **STT**: Sarvam Saaras v3 / OpenAI Whisper.
- **LLM**: Google Gemini 2.5 Flash / OpenAI GPT-4o.
- **TTS**: OpenAI Nova / Sarvam Bulbul.

### 3. E.D.I.T.H. Tool Package (`edith/`)
- `edith/tools/diagnostics.py`: CPU, RAM, Disk, Network speed, Process monitoring.
- `edith/tools/protocols.py`: Protocol Edith, Sentry, Stealth, House Party, Overclock, Lockdown.
- `edith/tools/intelligence.py`: Real-time web search, URL fetcher, breaking news, stock tickers.
- `edith/tools/workspace.py`: Directory inspection & safe terminal command execution.
- `edith/memory.py`: Persistent JSON key-value store & task roster.

### 4. Ultron 3D Holographic Core (`ultron/` & `hud/`)
- Three.js icosahedron wireframe shells with glowing inner core and particle physics.
- MediaPipe HandLandmarker webcam gesture tracking (pinch to rotate, two-hand pinch to zoom).
