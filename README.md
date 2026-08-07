# E.V.A.I. — Intelligent Digital Assistant

A Tony Stark-inspired digital assistant combining a real-time voice pipeline/MCP backend with an interactive 3D holographic orb interface.

---

## Repository Components

1. **[Interactive Frontend (ULTRON Orb UI)](#1-interactive-frontend-ultron-orb-ui)**: Next.js + Three.js holographic orb controlled by webcam hand gestures.
2. **[Voice Backend (E.V. — Tony Stark Demo)](#2-voice-backend-ev-tony-stark-demo)**: LiveKit voice pipeline agent and FastMCP server.

---

## 1. Interactive Frontend (ULTRON Orb UI)

An Iron Man–inspired holographic orb built with **Next.js**, **Three.js**, and **MediaPipe** hand tracking — control it with your bare hands through your webcam.

> 🔮 This is the open-source **interface** of [ULTRON](https://sagartamang.com/projects/ultron) — my AI that talks in real time and controls Android devices by itself. **[Read the write-up](https://sagartamang.com/projects/ultron)** or **[the X post](https://x.com/sagar_builds/status/2077277583646101921)**
> 📱 **[Watch the demo on Instagram](https://www.instagram.com/p/DayJ17OTwvx/)**

![ULTRON orb UI](docs/screenshot.png)

### Getting started (Frontend)

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Controls

#### Mouse / touch

| Input | Action |
| --- | --- |
| Drag | Spin the orb |
| Scroll / pinch | Zoom in & out |

#### Hand gestures (webcam)

Click **GESTURES OFF** (or press `G`) and allow camera access, then:

| Gesture | Action |
| --- | --- |
| Pinch (thumb + index) one hand and move it | Spin the orb |
| Pinch with **both** hands, spread apart / bring together | Zoom in / out |

#### Keyboard

| Key | Action |
| --- | --- |
| `G` | Toggle hand gestures |
| `R` | Reset the view |
| `+` / `−` | Zoom in / out |

---

## 2. Voice Backend (E.V. — Tony Stark Demo)

🎉 **Official Public Release:** E.V. is now officially released to the public as a standalone application! You can easily install it without needing to set up the development environment.

* **Download:** Visit [http://friday.feynmanpi.com/](http://friday.feynmanpi.com/)
* **Installers Available:** `.exe` for Windows and `.dmg` for macOS.

> *"Fully Responsive Intelligent Digital Assistant for You"*

A Tony Stark-inspired AI assistant split into two cooperating pieces:

| Component | What it is |
| --- | --- |
| **MCP Server** (`uv run friday`) | A [FastMCP](https://github.com/jlowin/fastmcp) server that exposes tools (news, web search, system info, …) over SSE. Think of it as the Stark Industries backend — it does the actual work. |
| **Voice Agent** (`uv run friday_voice`) | A [LiveKit Agents](https://github.com/livekit/agents) voice pipeline that listens to your microphone, reasons with an LLM (Gemini 2.5 Flash by default), and speaks back with OpenAI TTS — all while pulling tools from the MCP server in real time. |

**Demo:** [Instagram reel](https://www.instagram.com/p/DW2HjYtkwg_/)

### How it works (Backend)

```text
Microphone ──► STT (Sarvam Saaras v3)
                    │
                    ▼
             LLM (Gemini 2.5 Flash)  ◄──────► MCP Server (FastMCP / SSE)
                    │                              ├─ get_world_news
                    ▼                              ├─ open_world_monitor
             TTS (OpenAI nova)                     ├─ search_web
                    │                              └─ …more tools
                    ▼
             Speaker / LiveKit room
```

The voice agent connects to the MCP server via SSE at `http://127.0.0.1:8000/sse` (auto-resolved to the Windows host IP when running inside WSL).

### Quick start (Voice Backend - For Developers)

#### 1. Prerequisites

* Python ≥ 3.11
* [`uv`](https://github.com/astral-sh/uv) — run `pip install uv` or `curl -Lsf https://astral.sh/uv/install.sh | sh`
* A [LiveKit Cloud](https://cloud.livekit.io) project (the free tier works)

#### 2. Install dependencies

```bash
uv sync
```

*(This creates the .venv and installs all dependencies)*

#### 3. Set up environment

```bash
cp .env.example .env
```

*(Open the newly created `.env` file and fill in your API keys using the reference below)*

#### 4. Run — two terminals

**Terminal 1 — MCP server** (must start first)

```bash
uv run friday
```

Starts the FastMCP server on `http://127.0.0.1:8000/sse`. The voice agent connects here to fetch its tools.

**Terminal 2 — Voice agent**

```bash
uv run friday_voice
```

Starts the LiveKit voice agent in **dev mode** — it joins a LiveKit room and begins listening. Open the [LiveKit Agents Playground](https://agents-playground.livekit.io) and connect to your room to talk to FRIDAY.

---

## License

MIT
