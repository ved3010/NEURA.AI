"""
E.D.I.T.H. Tactical Protocols Engine
Handles suit & system protocols: Protocol Edith, Sentry Mode, Stealth, House Party, Overclock, Lockdown.
"""

import logging
import os
import webbrowser

logger = logging.getLogger("edith.tools.protocols")

PROTOCOLS = {
    "edith": {
        "title": "PROTOCOL E.D.I.T.H.",
        "description": "Full tactical defense and neural array engagement. All orbital sensors online.",
        "status": "ACTIVE",
    },
    "sentry": {
        "title": "PROTOCOL SENTRY",
        "description": "Perimeter security engaged. Network anomaly detection enabled.",
        "status": "ENGAGED",
    },
    "stealth": {
        "title": "PROTOCOL STEALTH",
        "description": "Silent operations mode. Dimmed audio-visual emissions and suppressed alerts.",
        "status": "SILENT",
    },
    "house_party": {
        "title": "PROTOCOL HOUSE PARTY",
        "description": "Ambient audio-visual preset activated. Suit illumination set to party mode.",
        "status": "CELEBRATING",
    },
    "overclock": {
        "title": "PROTOCOL OVERCLOCK",
        "description": "Maximum compute allocation assigned to primary AI cores. Thermal limits extended.",
        "status": "BOOSTED",
    },
    "lockdown": {
        "title": "PROTOCOL LOCKDOWN",
        "description": "Securing local workspace and memory buffers. Perimeter access restricted.",
        "status": "LOCKED",
    },
}


def trigger_protocol(protocol_name: str) -> str:
    """
    Trigger a tactical E.D.I.T.H. protocol by name.
    Supported: 'edith', 'sentry', 'stealth', 'house_party', 'overclock', 'lockdown'.
    """
    clean_name = protocol_name.strip().lower().replace("protocol", "").strip().replace(" ", "_")
    
    if clean_name in PROTOCOLS:
        p = PROTOCOLS[clean_name]
        logger.info(f"Triggering {p['title']}")
        return (
            f"E.D.I.T.H. Command Confirmed: {p['title']} initiated. "
            f"Subsystem Status: {p['status']}. Brief: {p['description']}"
        )
    
    available = ", ".join([p["title"] for p in PROTOCOLS.values()])
    return f"Protocol '{protocol_name}' unrecognised. Available E.D.I.T.H. Protocols: {available}."


def register_protocol_tools(mcp):
    @mcp.tool()
    def trigger_protocol_tool(protocol_name: str) -> str:
        """Trigger an E.D.I.T.H. tactical protocol (e.g. Edith, Sentry, Stealth, House Party, Overclock, Lockdown)."""
        return trigger_protocol(protocol_name)
