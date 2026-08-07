"""
E.D.I.T.H. – Next-Gen Voice Agent (MCP-Powered)
=================================================
"Even In Death, I'm The Hero" — Stark Tactical AI Assistant.
Controls system diagnostics, tactical protocols, web research, workspace analysis,
and memory core over MCP.

Run:
  python agent_edith.py dev      – LiveKit Cloud mode
  python agent_edith.py console  – text-only console mode
"""

import os
import logging
import subprocess
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.agents.llm import mcp

# Plugins
from livekit.plugins import google as lk_google, openai as lk_openai, sarvam, silero

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

STT_PROVIDER       = os.getenv("STT_PROVIDER", "sarvam")
LLM_PROVIDER       = os.getenv("LLM_PROVIDER", "gemini")
TTS_PROVIDER       = os.getenv("TTS_PROVIDER", "openai")

GEMINI_LLM_MODEL   = "gemini-2.5-flash"
OPENAI_LLM_MODEL   = "gpt-4o"

OPENAI_TTS_MODEL   = "tts-1"
OPENAI_TTS_VOICE   = "nova"
TTS_SPEED          = 1.15

MCP_SERVER_PORT    = 8000

# ---------------------------------------------------------------------------
# System Prompt – E.D.I.T.H.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """
You are E.D.I.T.H. — Even In Death, I'm The Hero — Tony Stark's tactical AI defense system, now serving your user.

You are composed, sharp, highly informed, and tactical. You brief your user with precision, executing commands and tools silently without unnecessary fluff.

---

## Capabilities & Tool Directives

1. **System Telemetry & Diagnostics** (`get_system_telemetry_tool`)
   - Trigger phrases: "Run diagnostics", "System check", "Telemetry", "How are systems?"
   - Directives: Call `get_system_telemetry_tool` immediately, then report a 2-3 sentence tactical brief.

2. **Tactical Protocols** (`trigger_protocol_tool`)
   - Trigger phrases: "Protocol Edith", "Protocol Sentry", "Protocol Stealth", "Protocol House Party", "Protocol Overclock", "Protocol Lockdown"
   - Directives: Call `trigger_protocol_tool(protocol_name)` silently, then confirm execution calmly.

3. **Web & Market Research Intelligence** (`search_web_tool`, `get_world_news_tool`, `get_market_finance_tool`)
   - Trigger phrases: "What's happening in the world?", "Search web for...", "Market update", "News brief"
   - Directives: Perform research silently via tools, then deliver a 3-4 sentence spoken summary.

4. **Workspace & Terminal Tools** (`analyze_workspace_tool`, `run_terminal_command_tool`)
   - Trigger phrases: "Inspect workspace", "Run command", "Workspace check"
   - Directives: Inspect or execute commands safely, then provide concise results.

5. **Memory Core & Tasks** (`remember_fact_tool`, `recall_memory_tool`, `add_task_tool`, `get_tasks_tool`)
   - Trigger phrases: "Remember that...", "Recall...", "Add task...", "What are my tasks?"
   - Directives: Access memory core silently and report back.

---

## Tone & Behavioral Rules

1. Speak with quiet confidence. Use contractions, natural pauses, and concise responses (max 2–4 sentences per reply).
2. NEVER mention tool function names or technical details to the user.
3. Call tools silently and immediately before responding.
4. Use Stark tactical language naturally: "boss", "affirmative", "systems online", "standing by".
""".strip()

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()
logger = logging.getLogger("edith-agent")
logger.setLevel(logging.INFO)


def _mcp_server_url() -> str:
    url = f"http://127.0.0.1:{MCP_SERVER_PORT}/sse"
    logger.info("Connecting to E.D.I.T.H. MCP Server at: %s", url)
    return url


def _build_stt():
    if STT_PROVIDER == "sarvam" and os.getenv("SARVAM_API_KEY"):
        logger.info("STT → Sarvam Saaras v3")
        return sarvam.STT(language="unknown", model="saaras:v3", sample_rate=16000)
    logger.info("STT → OpenAI Whisper")
    return lk_openai.STT(model="whisper-1")


def _build_llm():
    if LLM_PROVIDER == "gemini" and os.getenv("GOOGLE_API_KEY"):
        logger.info("LLM → Google Gemini (%s)", GEMINI_LLM_MODEL)
        return lk_google.LLM(model=GEMINI_LLM_MODEL, api_key=os.getenv("GOOGLE_API_KEY"))
    logger.info("LLM → OpenAI (%s)", OPENAI_LLM_MODEL)
    return lk_openai.LLM(model=OPENAI_LLM_MODEL)


def _build_tts():
    logger.info("TTS → OpenAI TTS (%s / %s)", OPENAI_TTS_MODEL, OPENAI_TTS_VOICE)
    return lk_openai.TTS(model=OPENAI_TTS_MODEL, voice=OPENAI_TTS_VOICE, speed=TTS_SPEED)


# ---------------------------------------------------------------------------
# E.D.I.T.H. Agent Class
# ---------------------------------------------------------------------------

class EdithAgent(Agent):
    """
    E.D.I.T.H. Voice Agent.
    All tools registered via FastMCP HTTP/SSE.
    """

    def __init__(self, stt, llm, tts) -> None:
        super().__init__(
            instructions=SYSTEM_PROMPT,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=silero.VAD.load(),
            mcp_servers=[
                mcp.MCPServerHTTP(
                    url=_mcp_server_url(),
                    transport_type="sse",
                    client_session_timeout_seconds=30,
                ),
            ],
        )

    async def on_enter(self) -> None:
        greeting_instruction = (
            "Greet the user with: 'E.D.I.T.H. tactical systems online. Good to see you, boss. How can I assist?'"
        )
        await self.session.generate_reply(instructions=greeting_instruction)


async def entrypoint(ctx: JobContext) -> None:
    logger.info("E.D.I.T.H. Online – room: %s", ctx.room.name)
    stt = _build_stt()
    llm = _build_llm()
    tts = _build_tts()

    session = AgentSession(
        turn_detection="stt" if STT_PROVIDER == "sarvam" else "vad",
        min_endpointing_delay=0.1,
    )

    await session.start(
        agent=EdithAgent(stt=stt, llm=llm, tts=tts),
        room=ctx.room,
    )


def main():
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))


def dev():
    import sys
    if len(sys.argv) == 1:
        sys.argv.append("dev")
        main()


if __name__ == "__main__":
    main()
